import psutil

def get_network_connections():
    connections = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'ESTABLISHED' and conn.remote_address:
            try:
                process = psutil.Process(conn.pid)
                connections.append({
                    "pid": conn.pid,
                    "name": process.name(),
                    "remote_ip": conn.remote_address.ip,
                    "remote_port": conn.remote_address.port
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    return connections