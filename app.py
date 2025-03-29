from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from database.db import save_scan_result, get_scan_results
from utils.scanner import scan_ports
from utils.dns_lookup import get_dns_info, get_reverse_dns, get_dns_records
from utils.ssl_checkup import check_ssl_certificate
from utils.cms_detect import detect_cms
from utils.subdomain import find_subdomains
from utils.whois_lookup import get_whois_info
from utils.nmap_scan import advanced_nmap_scan
import os
import re

app = Flask(__name__)

# Ensure reports directory exists
REPORTS_DIR = "reports"
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

def format_report(results):
    """ Format scan results into a readable report """
    formatted_text = "🔍 CYBERSECURITY SCAN REPORT\n"
    formatted_text += "=" * 50 + "\n\n"

    for key, value in results.items():
        formatted_text += f"🔹 {key.replace('_', ' ').title()}:\n"
        formatted_text += "-" * 30 + "\n"

        if isinstance(value, str):
            formatted_text += f"{value}\n\n"
        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                formatted_text += f"  - {sub_key.replace('_', ' ').title()}: {sub_value}\n"
            formatted_text += "\n"
        elif isinstance(value, list):
            for item in value:
                formatted_text += f"  - {item}\n"
            formatted_text += "\n"
        else:
            formatted_text += "❌ No data available\n\n"

    formatted_text += "=" * 50 + "\n"
    formatted_text += "📌 End of Report\n"

    return formatted_text
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        target = request.form["target"]
        scan_type = request.form.get("scan_type")  # User selects scan type

        scan_results = {}

        # Perform scans based on user selection
        if scan_type == "ports":
            scan_results["ports"] = scan_ports(target)
        elif scan_type == "dns":
            scan_results["dns_info"] = get_dns_info(target)
            scan_results["reverse_dns"] = get_reverse_dns(target)
            scan_results["dns_records"] = get_dns_records(target)
        elif scan_type == "ssl":
            scan_results["ssl_info"] = check_ssl_certificate(target)
        elif scan_type == "cms":
            scan_results["cms_info"] = detect_cms(target)
        elif scan_type == "subdomains":
            scan_results["subdomains"] = find_subdomains(target)
        elif scan_type == "whois":
            scan_results["whois_info"] = get_whois_info(target)
        elif scan_type == "nmap":
            scan_results["nmap_results"] = advanced_nmap_scan(target)
        else:
            scan_results = {
                "ports": scan_ports(target),
                "dns_info": get_dns_info(target),
                "reverse_dns": get_reverse_dns(target),
                "dns_records": get_dns_records(target),
                "ssl_info": check_ssl_certificate(target),
                "cms_info": detect_cms(target),
                "subdomains": find_subdomains(target),
                "whois_info": get_whois_info(target),
                "nmap_results": advanced_nmap_scan(target),
            }

        # Save results to MongoDB
        save_scan_result(target, scan_type or "full_scan", scan_results)

        # Save scan results to a report file
        safe_target = re.sub(r'[^a-zA-Z0-9.-]', '_', target)  # Remove invalid characters
        output_filename = f"{safe_target}.txt"
        output_path = os.path.join(REPORTS_DIR, output_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(format_report(scan_results))

        return render_template("results.html", target=target, results=scan_results)

    return render_template("index.html")

@app.route('/download/<filename>')
def download_file(filename):
    """ Route to serve the report file for download """
    file_path = os.path.join(REPORTS_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found!", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
