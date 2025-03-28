import requests
import re

API_KEY = "w2i2ewl93o1kbsans7lrrv2gvnxct7vbiwmb3l12b1hc8nvkhync3wlsk8p61mrwuig2iw"

def detect_cms(target):
    """Detect CMS from a given URL, domain, or IP address."""
    
    if not target.startswith("http"):
        target = "http://" + target  # Ensure it works for domains/IPs

    result = {"Target": target, "CMS": "Unknown"}

    # 🔹 Step 1: Try WhatCMS API
    try:
        api_url = f"https://whatcms.org/API/Tech?key={API_KEY}&url={target}"
        response = requests.get(api_url)
        data = response.json()

        if data.get("result", {}).get("code") == 200:
            result["CMS"] = data["result"]["name"]
            return result  # If API finds CMS, return immediately
    except Exception as e:
        print(f"⚠️ WhatCMS API Failed: {e}")

    # 🔹 Step 2: Try Manual CMS Detection (Headers & URLs)
    try:
        print(f"🟢 Checking Headers & URLs for {target}...")
        headers = requests.get(target).headers

        if "x-powered-by" in headers:
            result["CMS"] = headers["x-powered-by"]
            return result

        cms_patterns = {
            "WordPress": ["/wp-login.php"],
            "Joomla": ["/administrator"],
            "Drupal": ["/misc/drupal.js", "/sites/default/files"],
            "TYPO3": ["/typo3conf"],
            "Magento": ["/skin/frontend"]
        }

        for cms, paths in cms_patterns.items():
            for path in paths:
                if requests.get(f"{target}{path}").status_code == 200:
                    result["CMS"] = cms
                    return result
    except Exception as e:
        print(f"⚠️ Manual Detection Failed: {e}")

    return result
