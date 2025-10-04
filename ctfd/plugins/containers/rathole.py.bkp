import os
import requests

RAT_API_USERNAME = os.getenv('RAT_API_USERNAME')
RAT_API_PASSWORD = os.getenv('RAT_API_PASSWORD')
RAT_API1_HOST = os.getenv('RAT_API1_HOST')
RAT_API1_PORT = os.getenv('RAT_API1_PORT')
RAT_API2_HOST = os.getenv('RAT_API2_HOST')
RAT_API2_PORT = os.getenv('RAT_API2_PORT')

def start_tunnel(container_id, port):
    requests.post(
        f"http://{RAT_API1_HOST}:{RAT_API1_PORT}/start_tunnel",
        json={
            "container_id": f"ctfd-{container_id}",
            "container_port": port,
            "public_port": port
        },
        auth=(RAT_API_USERNAME, RAT_API_PASSWORD)
    )

    requests.post(
        f"http://{RAT_API2_HOST}:{RAT_API2_PORT}/start_tunnel",
        json={
            "container_id": f"ctfd-{container_id}",
            "container_port": port,
            "public_port": port
        },
        auth=(RAT_API_USERNAME, RAT_API_PASSWORD)
    )

def stop_tunnel(container_id):
    requests.post(
        f"http://{RAT_API1_HOST}:{RAT_API1_PORT}/stop_tunnel",
        json={
            "container_id": f"ctfd-{container_id}"
        },
        auth=(RAT_API_USERNAME, RAT_API_PASSWORD)
    )

    requests.post(
        f"http://{RAT_API2_HOST}:{RAT_API2_PORT}/stop_tunnel",
        json={
            "container_id": f"ctfd-{container_id}"
        },
        auth=(RAT_API_USERNAME, RAT_API_PASSWORD)
    )