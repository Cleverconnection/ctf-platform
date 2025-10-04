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

def get_ip(vmid, timeout=5):
    """Tenta obter IP IPv4 via qemu-guest-agent"""
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            res = px.nodes(node).qemu(vmid).agent("network-get-interfaces").get()
            for itf in res.get("result", []):
                for addr in itf.get("ip-addresses", []):
                    ip = addr.get("ip-address")
                    if ip and ":" not in ip and not ip.startswith("127."):
                        return ip
        except Exception:
            pass
        time.sleep(1)
    return "-"

# --- Execução ---
resources = px.cluster.resources.get(type="vm")

for r in resources:
    vid = int(r["vmid"])
    if vid < range_start or vid > range_end:
        continue
    name = r.get("name", "")
    if not name.startswith(name_prefix):
        continue
    status = r.get("status", "unknown")
    ip = get_ip(vid)
    print(f"{vid:5}  {name:40}  {status:10}  {ip}")

