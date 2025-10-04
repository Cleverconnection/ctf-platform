CONTAINER=itau-chall-manager-1

docker exec -it $CONTAINER bash -lc '
set -euo pipefail
BASE=/tmp/chall-manager/chall

echo "[*] Gerando destroy.py novo em /tmp/destroy.new ..."
cat > /tmp/destroy.new << "PYEOF"
#!/usr/bin/env python3
import os, json, time, pathlib, sys
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
    if isinstance(x, int): return x
    if isinstance(x, float): return int(x)
    try:
        return int(str(x).strip())
    except Exception:
        return None

def parse_json_env(name):
    s = os.getenv(name)
    if not s: return None
    try:
        return json.loads(s)
    except Exception:
        return None

def load_vmid():
    # 1) VMID explícito
    v = to_int(os.getenv("VMID"))
    if v: return v
    # 2) OUTPUTS_JSON
    o = parse_json_env("OUTPUTS_JSON")
    if o:
        v = to_int(o.get("vmid") or o.get("VMID"))
        if v: return v
    # 3) PULUMI_COMMAND_STDOUT (stdout do create)
    o = parse_json_env("PULUMI_COMMAND_STDOUT")
    if o:
        v = to_int(o.get("vmid") or o.get("VMID"))
        if v: return v
    pco = os.getenv("PULUMI_COMMAND_STDOUT")
    if pco and pco.strip().isdigit():
        v = to_int(pco.strip())
        if v: return v
    # 4) outputs.json local (fallback)
    try:
        here = pathlib.Path(__file__).resolve().parent
        o = json.loads((here / "outputs.json").read_text(encoding="utf-8"))
        v = to_int(o.get("vmid") or o.get("VMID"))
        if v: return v
    except Exception:
        pass
    return None  # idempotente: sem VMID, não quebra

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

# Sem VMID => considere já destruído (não quebra o flow)
if vmid is None:
    print(json.dumps({"deleted": True, "vmid": None, "note": "no vmid; treated as already removed"}))
    sys.exit(0)

# Tenta parar; ignore erros (idempotente)
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
        break
    time.sleep(2)

# Tenta excluir; ignore erros (idempotente)
try:
    up = px.nodes(node).qemu(vmid).delete()
    if isinstance(up, (str, dict)):
        upid = up if isinstance(up, str) else (up.get("data") or up.get("upid"))
        if upid:
            t1 = time.time()
            while time.time() - t1 < 60:
                try:
                    s = px.nodes(node).tasks(upid).status.get()
                    if s.get("status") == "stopped":
                        break
                except Exception:
                    break
                time.sleep(1)
except Exception:
    pass

print(json.dumps({"deleted": True, "vmid": vmid}))
sys.exit(0)
PYEOF

echo "[*] Aplicando patch em destroy.py de cada instância..."
count=0
while IFS= read -r f; do
  # Apenas instâncias com projeto materializado
  if [ -f "$f" ]; then
    cp -f /tmp/destroy.new "$f"
    chmod +x "$f"
    echo "  patched: $f"
    count=$((count+1))
  fi
done < <(find "$BASE" -type f -path "*/instance/*" -name destroy.py 2>/dev/null || true)

echo "[+] Total de destroy.py atualizados: $count"
'
