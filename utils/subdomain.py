import requests

def find_subdomains(target):
    """Finds subdomains of the target using a predefined wordlist"""
    subdomains = ["www", "mail", "ftp", "test", "dev", "blog", "admin", "api"]
    found_subdomains = []

    for sub in subdomains:
        url = f"http://{sub}.{target}"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                found_subdomains.append(f"{sub}.{target}")
        except requests.exceptions.RequestException:
            pass  # Ignore failed requests

    return found_subdomains if found_subdomains else ["No subdomains found"]

