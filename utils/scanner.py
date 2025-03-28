import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(target, port):
    """Scans a single port on the target"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        try:
            if s.connect_ex((target, port)) == 0:
                return f"Port {port} is OPEN"
        except socket.gaierror:
            return None  # Ignore invalid hostname
    return None

def scan_ports(target, start_port=1, end_port=1024):
    """Scans multiple ports using threading for efficiency"""
    try:
        # Check if the domain can be resolved
        socket.gethostbyname(target)
    except socket.gaierror:
        return {"Error": "Invalid hostname or DNS resolution failed"}

    open_ports = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(lambda port: scan_port(target, port), range(start_port, end_port + 1))

    return [result for result in results if result]
