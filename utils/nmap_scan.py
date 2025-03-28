import nmap

def advanced_nmap_scan(target):
    """Performs an advanced Nmap scan on the target."""
    try:
        scanner = nmap.PortScanner()
        scanner.scan(target, arguments="-A -T4")

        results = {}

        for host in scanner.all_hosts():
            results["IP"] = host
            results["State"] = scanner[host].state()

            for proto in scanner[host].all_protocols():
                results[proto] = []
                for port in scanner[host][proto].keys():
                    results[proto].append({
                        "Port": port,
                        "State": scanner[host][proto][port]['state'],
                        "Service": scanner[host][proto][port]['name']
                    })

        return results if results else {"Error": "No scan results found."}

    except Exception as e:
        return {"Error": f"Nmap scan failed: {str(e)}"}
