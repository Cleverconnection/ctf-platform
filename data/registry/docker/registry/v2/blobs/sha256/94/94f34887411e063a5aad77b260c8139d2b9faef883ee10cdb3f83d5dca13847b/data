#!/usr/bin/env python3
"""
Cria VM no Proxmox a partir de um template e retorna APENAS o IP em JSON.
- VMID escolhido dentro de um range (padrão: 2500–2700), configurável via:
  VMID_RANGE_START, VMID_RANGE_END
- Placa de rede e1000; por padrão preserva a net0 do template (inclui VLAN/tag).
  Se quiser sobrescrever a VLAN, use NET_VLAN_TAG=<tag> (opcional).
- IP via cloud-init: ipconfig0=dhcp
- CLONE_MODE=linked (padrão) ou full

ENVs necessárias:
  PROXMOX_API_URL=https://<host>:8006/api2/json
  PROXMOX_USER=<user>@pve
  PROXMOX_PASSWORD=<secret>
  PROXMOX_NODE=<node>                # ex.: cecpa
  PROXMOX_DATASTORE=local-lvm        # usado no full clone
  TEMPLATE_VMID=<vmid_template>      # ex.: 9000
  VM_CORES=2
  VM_MEMORY_MB=2048
  CLONE_MODE=linked|full             # default: linked
  NET_VLAN_TAG=<opcional>
  VMID_RANGE_START=2500 (opcional)
  VMID_RANGE_END=2700   (opcional)
"""

import os
import time
import json
from proxmoxer import ProxmoxAPI
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def env(name, default=None, required=False):
    v = os.getenv(name, default)
    if required and (v is None or v == ""):
        raise SystemExit(f"Missing env: {name}")
    return v

# --- Infra ---
api_url   = env("PROXMOX_API_URL", required=True)
user      = env("PROXMOX_USER", required=True)
password  = env("PROXMOX_PASSWORD", required=True)
verify    = (env("PROXMOX_VERIFY_SSL", "false").lower() != "false")
node      = env("PROXMOX_NODE", required=True)
datastore = env("PROXMOX_DATASTORE", "local-lvm")

# --- Parâmetros ---
template_vmid = int(env("TEMPLATE_VMID", required=True))
cores         = int(env("VM_CORES", "2"))
memory_mb     = int(env("VM_MEMORY_MB", "2048"))
net_bridge    = env("NET_BRIDGE", "vmbr0")     # usado apenas se sobrescrever net0
vlan_tag      = env("NET_VLAN_TAG", "")        # opcional
clone_mode    = env("CLONE_MODE", "linked").lower()  # linked|full

range_start   = int(env("VMID_RANGE_START", "2500"))
range_end     = int(env("VMID_RANGE_END", "2700"))

# --- Conexão ---
host = api_url.split("/api2/json")[0].replace("https://","").replace("http://","").strip("/")
px = ProxmoxAPI(host=host, user=user, password=password, verify_ssl=verify)

def upid_of(resp):
    if isinstance(resp, str):
        return resp
    if isinstance(resp, dict):
        return resp.get("data") or resp.get("upid") or next(iter(resp.values()), None)
    return None

def wait_task(upid):
    if not upid:
        raise SystemExit("UPID inválido ao iniciar tarefa no Proxmox")
    while True:
        s = px.nodes(node).tasks(upid).status.get()
        if s.get("status") == "stopped":
            if s.get("exitstatus") == "OK":
                return
            raise SystemExit(f"Task failed: {s}")
        time.sleep(1)

def nextid_in_range(start: int, end: int) -> int:
    used = {int(v["vmid"]) for v in px.cluster.resources.get(type="vm")}
    for vid in range(start, end + 1):
        if vid not in used:
            return vid
    raise SystemExit(f"Nenhum VMID livre entre {start}-{end}")

# --- Reserva VMID dentro do range ---
vmid = nextid_in_range(range_start, range_end)

# --- Clone do template ---
if clone_mode == "linked":
    clone_resp = px.nodes(node).qemu(template_vmid).clone.post(
        newid=vmid, full=0, target=node
    )
else:
    clone_resp = px.nodes(node).qemu(template_vmid).clone.post(
        newid=vmid, full=1, target=node, storage=datastore
    )
wait_task(upid_of(clone_resp))

# --- Configuração mínima do clone ---
cfg = dict(
    cores=cores,
    memory=memory_mb,
    agent=1,
    ciuser="ctf",
    ipconfig0="ip=dhcp",
)

# Preserva net0 do template; sobrescreve apenas se NET_VLAN_TAG vier
if vlan_tag:
    cfg["net0"] = f"e1000,bridge={net_bridge},tag={vlan_tag}"

px.nodes(node).qemu(vmid).config.post(**cfg)

# --- Liga VM ---
start_resp = px.nodes(node).qemu(vmid).status.start.post()
wait_task(upid_of(start_resp))

# --- Pega IP via guest-agent ---
def get_ip(timeout=240):
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
        time.sleep(2)
    return None

ip = get_ip()
if not ip:
    raise SystemExit("Falha ao obter IP via qemu-guest-agent (verifique cloud-init, agent e DHCP).")

# --- Saída mínima: SOMENTE IP ---
print(json.dumps({"ip": ip}))
