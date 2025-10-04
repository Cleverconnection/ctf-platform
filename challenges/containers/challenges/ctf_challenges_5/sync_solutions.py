#!/usr/bin/env python3
import os, glob, requests, yaml

CTFD_URL     = os.environ.get("CTFD_URL", "http://localhost:8000").rstrip("/")
CTFD_TOKEN   = os.environ.get("CTFD_TOKEN")
CTFD_SESSION = os.environ.get("CTFD_SESSION")

if not CTFD_TOKEN or not CTFD_SESSION:
    print("❌ ERRO: export CTFD_TOKEN e CTFD_SESSION antes de rodar")
    exit(1)

HEADERS_TOKEN   = {"Authorization": f"Token {CTFD_TOKEN}"}
HEADERS_SESSION = {"Cookie": f"session={CTFD_SESSION}"}

def find_challenge_id(name):
    url = f"{CTFD_URL}/api/v1/challenges?view=admin"
    r = requests.get(url, headers=HEADERS_SESSION)
    if not r.ok:
        print(f"❌ Erro ao listar challenges: {r.status_code} {r.text[:200]}")
        return None
    for ch in r.json().get("data", []):
        if ch["name"] == name:
            return ch["id"]
    return None

def get_existing_solution(cid):
    url = f"{CTFD_URL}/api/v1/solutions"
    r = requests.get(url, headers=HEADERS_SESSION)  # usa session!
    if not r.ok:
        print(f"❌ Erro ao listar solutions: {r.status_code} {r.text[:200]}")
        return None
    for s in r.json().get("data", []):
        if s["challenge_id"] == cid:
            return s
    return None

def upsert_solution(cid, content, state="hidden"):
    existing = get_existing_solution(cid)
    payload = {"challenge_id": cid, "content": content, "state": state}
    if existing:
        sid = existing["id"]
        url = f"{CTFD_URL}/api/v1/solutions/{sid}"
        r = requests.patch(url, headers=HEADERS_TOKEN, json=payload)
        print(f"PATCH solution {sid} -> {r.status_code}")
    else:
        url = f"{CTFD_URL}/api/v1/solutions"
        r = requests.post(url, headers=HEADERS_TOKEN, json=payload)
        print(f"POST solution cid={cid} -> {r.status_code}")
    if not r.ok:
        print("❌ Erro:", r.status_code, r.text[:200])
    r.raise_for_status()

def main():
    for chal_dir in glob.glob("E*/"):
        chal_file = os.path.join(chal_dir, "challenge.yml")
        writeup   = os.path.join(chal_dir, "WRITEUP.md")
        if not (os.path.isfile(chal_file) and os.path.isfile(writeup)):
            continue

        with open(chal_file, "r", encoding="utf-8") as f:
            yml = yaml.safe_load(f)
        name = yml.get("name")

        print(f"\n=== {name} ({chal_dir}) ===")
        cid = find_challenge_id(name)
        if not cid:
            print(f"[WARN] Challenge '{name}' não encontrado")
            continue

        with open(writeup, "r", encoding="utf-8") as f:
            content = f.read()

        upsert_solution(cid, content, state="hidden")
        print(f"[OK] Solução sincronizada: {name}")

if __name__ == "__main__":
    main()

