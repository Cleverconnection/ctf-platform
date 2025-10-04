import os, time
from proxmoxer import ProxmoxAPI
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ------------------------------
# Configuração ambiente
# ------------------------------
def env(name, default=None, required=False):
    v = os.getenv(name, default)
    if required and (v is None or v == ""):
        raise SystemExit(f"Missing env: {name}")
    return v

api_url   = env("PROXMOX_API_URL", required=True)
user      = env("PROXMOX_USER", required=True)
password  = env("PROXMOX_PASSWORD", required=True)
verify    = (env("PROXMOX_VERIFY_SSL", "false").lower() != "false")
node      = env("PROXMOX_NODE", "cecpa")
datastore = env("PROXMOX_DATASTORE", "local-lvm")

template_vmid = int(env("TEMPLATE_VMID", "2221"))

# usernames fixos (30)
usernames = [
    "mateus.balabenute",
    "felipe.oliveira",
    "rogerio.silva",
    "thomaz.ribeiro",
    "kaique.lima",
    "claudevan.silva",
    "alexandre.lima",
    "jessica.sousa",
    "pedro.quinaia",
    "gustavo.pereira",
    "daniel.santos",
    "patrick.nascimento",
    "marcos.tolosa",
    "ricardo.souza",
    "acacio.martins",
    "fernanda.fahl",
    "lucas.saito",
    "alan.viana",
    "douglas.carvalho",
    "guilherme.galdino",
    "cleiton.silva",
    "caique.celoto",
    "bruno.lima",
    "alexandro.correa",
    "candida.paraizo",
    "valdei.rocha",
    "joao.boas",
    "danilo.santos",
    "vinicius.lima",
    "jaemilton.oliveira",
]

# range fixo 2222–2300
vmid_start = 2222

# ------------------------------
# Conexão Proxmox
# ------------------------------
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

def used_vmids():
    return {int(v["vmid"]) for v in px.cluster.resources.get(type="vm")}

def do_clone(vmid, name, mode="linked"):
    if mode == "linked":
        return px.nodes(node).qemu(template_vmid).clone.post(
            newid=vmid,
            name=name,
            full=0,
            target=node
        )
    else:
        return px.nodes(node).qemu(template_vmid).clone.post(
            newid=vmid,
            name=name,
            full=1,
            target=node,
            storage=datastore
        )

def configure_vm(vmid):
    cfg = dict(
        agent=1,
        onboot=1,
        ciuser="ctf",
        ipconfig0="ip=dhcp",
    )
    px.nodes(node).qemu(vmid).config.post(**cfg)

def start_vm(vmid):
    upid = upid_of(px.nodes(node).qemu(vmid).status.start.post())
    wait_task(upid)

# ------------------------------
# Execução
# ------------------------------
used = used_vmids()
for idx, username in enumerate(usernames):
    vmid = vmid_start + idx
    if vmid in used or vmid == template_vmid:
        continue
    vm_name = f"itau-participante-{username}"
    try:
        resp = do_clone(vmid, vm_name, "linked")
    except Exception as e:
        msg = str(e).lower()
        if "linked clone feature is not supported" in msg:
            resp = do_clone(vmid, vm_name, "full")
        else:
            raise
    wait_task(upid_of(resp))
    configure_vm(vmid)
    start_vm(vmid)

