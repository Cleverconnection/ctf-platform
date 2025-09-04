#!/usr/bin/env python3
import os, time, json
from proxmoxer import ProxmoxAPI
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def env(name, default=None, required=False):
    v = os.getenv(name, default)
    if required and (v is None or v == ""):
        raise SystemExit(f"Missing env: {name}")
    return v

api_url   = env("PROXMOX_API_URL", required=True)
user      = env("PROXMOX_USER", required=True)
password  = env("PROXMOX_PASSWORD", required=True)
verify    = (env("PROXMOX_VERIFY_SSL", "false").lower() != "false")
node      = env("PROXMOX_NODE", required=True)

action    = env("ACTION", "destroy").lower()
reset_type= env("RESET_TYPE", "soft").lower()

vmid = env("VMID")
if not vmid:
    out = env("OUTPUTS_JSON")
    if out:
        try:
            vmid = str(json.loads(out).get("vmid"))
        except Exception:
            pass
if not vmid:
    raise SystemExit("Defina VMID=... ou OUTPUTS_JSON='{\"vmid\":...}'")
vmid = int(vmid)

host = api_url.split("/api2/json")[0].replace("https://","").replace("http://","").strip("/")
px = ProxmoxAPI(host=host, user=user, password=password, verify_ssl=verify)

def wait_stopped(timeout=25):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            st = px.nodes(node).qemu(vmid).status.current.get()
            if st.get("status") in ("stopped", "", None):
                return True
        except Exception:
            return True
        time.sleep(1)
    return False

def safe_shutdown_then_stop():
    try: px.nodes(node).qemu(vmid).status.shutdown.post()
    except Exception: pass
    if not wait_stopped(20):
        try: px.nodes(node).qemu(vmid).status.stop.post()
        except Exception: pass
        wait_stopped(10)

if action == "destroy":
    safe_shutdown_then_stop()
    try:
        px.nodes(node).qemu(vmid).delete()
        print(json.dumps({"status": "destroyed", "vmid": vmid}))
    except Exception as e:
        print(json.dumps({"status": "destroyed_or_missing", "vmid": vmid, "detail": str(e)}))
elif action == "reset":
    if reset_type == "hard":
        try:
            px.nodes(node).qemu(vmid).status.reset.post()
            print(json.dumps({"status": "hard_reset", "vmid": vmid}))
        except Exception:
            safe_shutdown_then_stop()
            try:
                px.nodes(node).qemu(vmid).status.start.post()
                print(json.dumps({"status": "stop_start", "vmid": vmid}))
            except Exception as e:
                print(json.dumps({"status": "error", "vmid": vmid, "detail": str(e)}))
    else:
        try:
            px.nodes(node).qemu(vmid).status.reboot.post()
            print(json.dumps({"status": "soft_reboot", "vmid": vmid}))
        except Exception as e:
            print(json.dumps({"status": "error", "vmid": vmid, "detail": str(e)}))
elif action == "stop":
    safe_shutdown_then_stop()
    print(json.dumps({"status": "stopped", "vmid": vmid}))
elif action == "start":
    try:
        px.nodes(node).qemu(vmid).status.start.post()
        print(json.dumps({"status": "started", "vmid": vmid}))
    except Exception as e:
        print(json.dumps({"status": "error", "vmid": vmid, "detail": str(e)}))
else:
    raise SystemExit(f"ACTION desconhecida: {action}")

