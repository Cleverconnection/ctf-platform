import os, time
from proxmoxer import ProxmoxAPI
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def env(name, default=None, required=False):
    v = os.getenv(name, default)
    if required and (v is None or v == ""):
        raise SystemExit(f"Missing env: {name}")
    return v

# --- Infra obrigatória ---
api_url   = env("PROXMOX_API_URL", required=True)
user      = env("PROXMOX_USER", required=True)
password  = env("PROXMOX_PASSWORD", required=True)
verify    = (env("PROXMOX_VERIFY_SSL", "false").lower() != "false")
node      = env("PROXMOX_NODE", "cecpa")

range_start = int(env("VMID_RANGE_START", "2222"))
range_end   = int(env("VMID_RANGE_END",   "2300"))

name_prefix = env("VM_NAME_PREFIX", "itau-participante-")

# --- Conexão Proxmox ---
host = api_url.split("/api2/json")[0].replace("https://","").replace("http://","").strip("/")
px = ProxmoxAPI(host=host, user=user, password=password, verify_ssl=verify)

def upid_of(resp):
    if isinstance(resp, str): return resp
    if isinstance(resp, dict): return resp.get("data") or resp.get("upid") or next(iter(resp.values()), None)
    return None

def wait_task(upid):
    while True:
        s = px.nodes(node).tasks(upid).status.get()
        if s.get("status") == "stopped":
            if s.get("exitstatus") == "OK":
                return
            raise SystemExit(f"Tarefa falhou: {s}")
        time.sleep(1)

def list_vms():
    out = {}
    for r in px.cluster.resources.get(type="vm"):
        vid = int(r["vmid"])
        name = r.get("name", "")
        out[vid] = name
    return out

def restart_vm(vmid):
    # Se estiver rodando, faz shutdown
    try:
        status = px.nodes(node).qemu(vmid).status.current.get()
        if status.get("status") == "running":
            upid = upid_of(px.nodes(node).qemu(vmid).status.shutdown.post(forceStop=1))
            wait_task(upid)
    except Exception:
        pass
    # Start de novo
    upid = upid_of(px.nodes(node).qemu(vmid).status.start.post())
    wait_task(upid)

# --- Execução ---
vms = list_vms()

for vid in range(range_start, range_end+1):
    name = vms.get(vid)
    if not name:
        continue
    if not name.startswith(name_prefix):
        continue
    restart_vm(vid)

# Fim silencioso
