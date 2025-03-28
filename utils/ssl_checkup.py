import ssl
import socket
from datetime import datetime

def check_ssl_certificate(target):
    """Checks SSL certificate details of the target domain"""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((target, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=target) as ssock:
                cert = ssock.getpeercert()
                
                # Extract relevant SSL details
                issuer = dict(x[0] for x in cert["issuer"])
                issued_to = dict(x[0] for x in cert["subject"])["commonName"]
                valid_from = datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z")
                valid_until = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")

                return {
                    "Issued To": issued_to,
                    "Issuer": issuer["organizationName"],
                    "Valid From": valid_from.strftime("%Y-%m-%d"),
                    "Valid Until": valid_until.strftime("%Y-%m-%d"),
                    "Days Left": (valid_until - datetime.utcnow()).days
                }
    
    except Exception as e:
        return {"Error": f"SSL Check Failed: {str(e)}"}

