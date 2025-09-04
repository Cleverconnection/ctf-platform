import base64, hashlib, hmac, os, re, time, uuid
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import docker

# ========= Config =========
DOCKER_HOST    = os.getenv("DOCKER_HOST", "tcp://docker-socket-proxy:2375")
DOCKER_NETWORK = os.getenv("DOCKER_NETWORK", "ctf_net")
BASE_DOMAIN    = os.getenv("BASE_DOMAIN", "ctf.local")
TRAEFIK_ENTRY  = os.getenv("TRAEFIK_ENTRYPOINT", "websecure")
TRAEFIK_CERTRESOLVER = os.getenv("TRAEFIK_CERTRESOLVER", "le")  # deixe vazio para não setar
FLAG_SECRET    = os.getenv("FLAG_SECRET", "troque-esse-segredo")
API_SECRET     = os.getenv("SPAWNER_API_SECRET", "troque-esse-segredo-api")

SAFE = re.compile(r"[^a-z0-9-]")
def sanitize(s: str) -> str:
    return SAFE.sub("-", s.strip().lower())

class SpawnRequest(BaseModel):
    team: str = Field(..., examples=["team01"])
    challenge: str = Field(..., examples=["hello-web"])
    image: str = Field(..., examples=["ghcr.io/nginxinc/nginx-unprivileged:stable-alpine"])
    internal_port: int = Field(8080, ge=1, le=65535)
    cpu_quota: Optional[int] = 0         # em microssegundos (conteinerd): 100000 = 10% de um core
    mem_limit: Optional[str] = None      # ex: "512m"
    flag: Optional[str] = None
    ttl_minutes: Optional[int] = 0       # 0 = nunca expira (evite em produção)

class DestroyRequest(BaseModel):
    team: Optional[str] = None
    challenge: Optional[str] = None
    container_name: Optional[str] = None

api = FastAPI(title="CTF Spawner", version="1.1.0")
docker_client = docker.DockerClient(base_url=DOCKER_HOST)

def verify_hmac(raw: bytes, signature_b64url: str) -> bool:
    mac = hmac.new(API_SECRET.encode(), raw, hashlib.sha256).digest()
    expected = base64.urlsafe_b64encode(mac).decode().rstrip("=")
    return hmac.compare_digest(expected, signature_b64url or "")

@api.middleware("http")
async def hmac_auth(request: Request, call_next):
    if request.url.path in ("/healthz", "/", "/list"):
        return await call_next(request)
    sig = request.headers.get("x-signature", "")
    raw = await request.body()
    if not verify_hmac(raw, sig):
        return JSONResponse(status_code=401, content={"detail": "unauthorized"})
    return await call_next(request)

@api.get("/")
def root():
    return {"ok": True, "service": "spawner", "version": "1.1.0"}

@api.get("/healthz")
def healthz():
    try:
        docker_client.ping()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(500, f"docker ping failed: {e}")

def make_flag(team: str, challenge: str) -> str:
    payload = f"{team}:{challenge}:{uuid.uuid4()}"
    mac = hmac.new(FLAG_SECRET.encode(), payload.encode(), hashlib.sha256).digest()
    sig = base64.urlsafe_b64encode(mac).decode().rstrip("=")
    return f"CTF{{{payload}.{sig}}}"

def traefik_labels(host: str, service: str, port: int):
    labels = {
        "traefik.enable": "true",
        f"traefik.http.routers.{service}.rule": f"Host(`{host}`)",
        f"traefik.http.routers.{service}.entrypoints": TRAEFIK_ENTRY,
        f"traefik.http.services.{service}.loadbalancer.server.port": str(port),
    }
    # TLS automático (se desejar)
    if TRAEFIK_CERTRESOLVER:
        labels[f"traefik.http.routers.{service}.tls"] = "true"
        labels[f"traefik.http.routers.{service}.tls.certresolver"] = TRAEFIK_CERTRESOLVER
    return labels

def list_like(filters: dict):
    return docker_client.containers.list(all=True, filters=filters)

def next_sequence(team: str, challenge: str) -> int:
    """Conta instâncias anteriores para (team, challenge) e retorna próximo índice (1..N)."""
    flt = {"label": [f"ctf.kind=challenge-instance", f"ctf.team={team}", f"ctf.challenge={challenge}"]}
    existing = list_like(flt)
    # pega o maior ctf.seq já usado
    seqs: List[int] = []
    for c in existing:
        try:
            seqs.append(int((c.labels or {}).get("ctf.seq", "0")))
        except ValueError:
            continue
    return (max(seqs) if seqs else 0) + 1

@api.post("/spawn")
def spawn(req: SpawnRequest):
    team = sanitize(req.team)
    chal = sanitize(req.challenge)

    # gera sequência incremental e host único
    seq = next_sequence(team, chal)
    # ex.: hello-web-3.team01.ctf.dominio
    sub = f"{chal}-{seq}"
    service = f"{team}-{sub}-{int(time.time())}"  # service único p/ Traefik
    host = f"{sub}.{team}.{BASE_DOMAIN}"
    container_name = f"ctf_{service}"

    # tenta puxar imagem (best-effort)
    try:
        docker_client.images.pull(req.image)
    except Exception:
        pass

    # FLAG dinâmica (caso não venha pronta)
    flag_value = req.flag or make_flag(team, chal)

    env = {
        "FLAG": flag_value,
        "TEAM": team,
        "CHALLENGE": chal,
        "INSTANCE_SEQ": str(seq),
    }

    # Labels de metadados + Traefik
    labels = {
        "ctf.team": team,
        "ctf.challenge": chal,
        "ctf.kind": "challenge-instance",
        "ctf.host": host,
        "ctf.service": service,
        "ctf.seq": str(seq),
    }
    # TTL em epoch (se configurado) — útil para um reaper externo
    if req.ttl_minutes and req.ttl_minutes > 0:
        labels["ctf.expires_at"] = str(int(time.time()) + req.ttl_minutes * 60)

    labels.update(traefik_labels(host, service, req.internal_port))

    # Limites de recursos + auto_remove
    host_config = docker.types.HostConfig(
        auto_remove=True,
        cpu_quota=req.cpu_quota if (req.cpu_quota and req.cpu_quota > 0) else None,
        mem_limit=req.mem_limit if req.mem_limit else None,
    )

    try:
        container = docker_client.containers.create(
            req.image,
            name=container_name,
            detach=True,
            environment=env,
            labels=labels,
            host_config=host_config,
            network=DOCKER_NETWORK,
        )
        container.start()
    except Exception as e:
        raise HTTPException(500, f"container create/start failed: {e}")

    return {
        "ok": True,
        "container_name": container_name,
        "url": f"https://{host}/",
        "host": host,
        "service": service,
        "team": team,
        "challenge": chal,
        "seq": seq,
        "flag_injected": bool(req.flag is None),
    }

@api.post("/destroy")
def destroy(req: DestroyRequest):
    if not any([req.container_name, req.team, req.challenge]):
        raise HTTPException(400, "informe container_name OU team/challenge")

    if req.container_name:
        try:
            containers = [docker_client.containers.get(req.container_name)]
        except Exception:
            return {"ok": True, "destroyed": 0}
    else:
        filters = {"label": ["ctf.kind=challenge-instance"]}
        if req.team:
            filters["label"].append(f"ctf.team={sanitize(req.team)}")
        if req.challenge:
            filters["label"].append(f"ctf.challenge={sanitize(req.challenge)}")
        containers = list_like(filters)

    destroyed = 0
    for c in containers:
        try:
            c.remove(force=True)
            destroyed += 1
        except Exception:
            pass

    return {"ok": True, "destroyed": destroyed}

@api.get("/list")
def list_instances(team: Optional[str] = None, challenge: Optional[str] = None):
    filters = {"label": ["ctf.kind=challenge-instance"]}
    if team:
        filters["label"].append(f"ctf.team={sanitize(team)}")
    if challenge:
        filters["label"].append(f"ctf.challenge={sanitize(challenge)}")

    items = []
    for c in list_like(filters):
        labels = c.labels or {}
        items.append({
            "name": c.name,
            "id": c.id[:12],
            "status": c.status,
            "team": labels.get("ctf.team"),
            "challenge": labels.get("ctf.challenge"),
            "seq": labels.get("ctf.seq"),
            "host": labels.get("ctf.host"),
            "service": labels.get("ctf.service"),
            "expires_at": labels.get("ctf.expires_at"),
        })
    return {"ok": True, "instances": items}
