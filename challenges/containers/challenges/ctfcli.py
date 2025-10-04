# test_ctfd_api.py
import requests

url = "https://ctf-itau.cecyber.com/api/v1/challenges"
headers = {"Authorization": "Token ctfd_281e6aad460e805a12321c9f745425f4d7f664573243adf955f56ed6cbef426d"}
r = requests.get(url, headers=headers, verify="/home/user/itau/challenges/containers/challenges/ctfd.crt")
print(r.status_code)
print(r.text[:500])
