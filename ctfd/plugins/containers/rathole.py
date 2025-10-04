# CTFd plugin patch - Rathole desativado
# Este arquivo substitui o rathole.py original

def start_tunnel(container_id, port):
    """
    Rathole desativado. O Traefik já cuida da exposição
    dos containers via wildcard DNS.
    """
    print(f"[INFO] start_tunnel ignorado para container {container_id} (porta {port})")
    return


def stop_tunnel(container_id):
    """
    Rathole desativado. Nada a fazer.
    """
    print(f"[INFO] stop_tunnel ignorado para container {container_id}")
    return
