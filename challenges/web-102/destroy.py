#!/usr/bin/env python3
import os, json, time, pathlib
from proxmoxer import ProxmoxAPI
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def env(name, default=None, required=False):
    v = os.getenv(name, default)
    if required and (v is None or v == ""):
        raise SystemExit(f"Missing env: {name}")
    return v

def to_int(x):
    if x is None: return None
    if isinstance(x, (int,)): return x
    if isinstance(x, float): return int(x)
    s = str(x).strip()
    try:
        return int(s)
    except Exception:
        return None

def load_vmid():
    # 1) VMID explícito
    v = to_int(os.getenv("VMID"))
    if v: return v

    # 2) OUTPUTS_JSON (se o orquestrador passar)
    j = os.getenv("OUTPUTS_JSON")
    if j:
        try:
            o = json.loads(j)
            v = to_int(o.get("vmid") or o.get("VMID"))
            if v: return v
        except Exception:
            pass

    # 3) PULUMI_COMMAND_STDOUT (Pulumi Command Provider injeta stdout do create)
    #    https://www.pulumi.com/registry/packages/command/api-docs/local/command/
    #    "The environment variables PULUMI_COMMAND_STDOUT and ... are set to the stdout ... from previous create/update steps."
    pco = os.getenv("PULUMI_COMMAND_STDOUT")
    if pco:
        try:
            o = json.loads(pco)
            v = to_int(o.get("vmid") or o.get("VMID"))
            if v: return v
        except Exception:
            # Se alguém imprimiu algo não-JSON, tentamos um parse básico de números
            s = pco.strip()
            if s.isdigit():
                v = to_int(s)
                if v: return v

    # 4) outputs.json no diretório do cenário (fallback)
    try:
        here = pathlib.Path(__file__).resolve().parent
        o = json.loads((here / "outputs.json").read_text(encoding="utf-8"))
        v = to_int(o.get("vmid") or o.get("VMID"))
        if v: return v
    except Exception:
        pass

    raise SystemExit("Defina VMID=... ou OUTPUTS_JSON='{\"vmid\":...}' (ou gere outputs.json / use PULUMI_COMMAND_STDOUT)")

# --- Infra ---
api_url   = env("PROXMOX_API_URL", required=True)
user      = env("PROXMOX_USER", required=True)
password  = env("PROXMOX_PASSWORD", required=True)
verify    = (env("PROXMOX_VERIFY_SSL", "false").lower() != "false")
node      = env("PROXMOX_NODE", "cecpa")

host = api_url.split("/api2/json")[0].replace("https://","").replace("http://","").strip("/")
px = ProxmoxAPI(host=host, user=user, password=password, verify_ssl=verify)

def upid_of(resp):
    if isinstance(resp, str): return resp
    if isinstance(resp, dict): return resp.get("data") or resp.get("upid") or next(iter(resp.values()), None)
    return None

def wait_task(upid, timeout=180):
    if not upid: return
    t0 = time.time()
    while time.time() - t0 < timeout:
        s = px.nodes(node).tasks(upid).status.get()
        if s.get("status") == "stopped":
            return
        time.sleep(1)

vmid = load_vmid()

# Tenta desligar, mas segue mesmo se já estiver parada/inexistente
try:
    px.nodes(node).qemu(vmid).status.stop.post()
except Exception:
    pass

# Aguarda parar
t0 = time.time()
while time.time() - t0 < 120:
    try:
        st = px.nodes(node).qemu(vmid).status.current.get()
        if st.get("status") != "running":
            break
    except Exception:
        # Se não achar mais a VM, considere como deletada
        break
    time.sleep(2)

# Exclui a VM (idempotente)
try:
    up = px.nodes(node).qemu(vmid).delete()
    wait_task(upid_of(up))
except Exception:
    # Se já foi removida, ok
    pass

print(json.dumps({"deleted": True, "vmid": vmid}))
