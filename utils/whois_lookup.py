import whois

def get_whois_info(domain):
    """ Fetch WHOIS info with improved error handling """
    try:
        if not domain or "." not in domain:
            return {"error": "Invalid domain format"}

        data = whois.whois(domain)
        
        if not data:
            return {"error": "WHOIS data not available"}

        return {
            "Domain Name": getattr(data, "domain_name", "N/A"),
            "Registrar": getattr(data, "registrar", "N/A"),
            "Creation Date": getattr(data, "creation_date", "N/A"),
            "Expiration Date": getattr(data, "expiration_date", "N/A"),
            "Name Servers": getattr(data, "name_servers", "N/A")
        }
    except Exception as e:
        return {"error": f"WHOIS Lookup Failed: {str(e)}"}
