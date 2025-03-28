import socket
import dns.resolver

def get_dns_info(target):
    """Performs DNS lookup and retrieves the target's IP address"""
    try:
        ip_address = socket.gethostbyname(target)
        return {"IP Address": ip_address}
    except socket.gaierror:
        return {"Error": "Could not resolve DNS"}

def get_reverse_dns(ip_address):
    try:
        host = socket.gethostbyaddr(ip_address)
        return host[0]
    except socket.herror:
        return "Reverse DNS not found"
    except socket.gaierror:
        return "Invalid IP or no DNS entry"

def get_dns_records(target):
    """Fetches A, MX, CNAME, and TXT records of the target"""
    records = {}
    record_types = ["A", "MX", "CNAME", "TXT"]
    
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(target, record_type)
            records[record_type] = [answer.to_text() for answer in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.LifetimeTimeout):
            records[record_type] = "No record found"
    
    return records
