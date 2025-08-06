# Domain-ThreatHunter

**Domain-ThreatHunter** is a Python-based reconnaissance tool that gathers passive intelligence on a target domain using WHOIS, DNS, SSL/TLS info, subdomain enumeration, ASN lookups, and reputation checks from VirusTotal.

## 🧰 Features

- WHOIS Lookup
- DNS Record Enumeration (A, MX, NS, TXT, etc.)
- SSL/TLS Certificate Details
- Reverse DNS Lookup
- ASN and Geolocation Info
- Web Server Fingerprinting
- VirusTotal Blacklist Check
- Passive Subdomain Enumeration (via crt.sh)

---

## 🖼️ Example Output

> _Add screenshots here to show example output for each section_  
> Suggested:
> - WHOIS output  
> - DNS records  
> - SSL cert info  
> - VirusTotal result  

---

## ⚙️ Setup (Using Virtual Environment)

```bash
# Clone domain_threathunter.py
# With curl
curl -O https://raw.githubusercontent.com/nothin-special/security-logs/main/Projects/Scripts/Blue/Domain-ThreatHunter/domain_threathunter.py && \
curl -O https://raw.githubusercontent.com/nothin-special/security-logs/main/Projects/Scripts/Blue/Domain-ThreatHunter/requirements.txt

# Or with wget
wget https://raw.githubusercontent.com/nothin-special/security-logs/main/Projects/Scripts/Blue/Domain-ThreatHunter/domain_threathunter.py && \
wget https://raw.githubusercontent.com/nothin-special/security-logs/main/Projects/Scripts/Blue/Domain-ThreatHunter/requirements.txt

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
