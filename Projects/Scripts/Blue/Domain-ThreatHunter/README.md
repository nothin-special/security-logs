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

> - WHOIS
<img width="942" height="360" alt="image" src="https://github.com/user-attachments/assets/d1649cf2-f8d1-43e9-80c1-533b99bdc4f8" />

> - DNS records
<img width="953" height="122" alt="image" src="https://github.com/user-attachments/assets/20054a6d-8980-445b-a388-91a89be08d95" />

> - SSL cert info  
<img width="774" height="144" alt="image" src="https://github.com/user-attachments/assets/c84b3b4e-fd35-4c9e-badb-2b1ea13d4f24" />

> - VirusTotal result  
<img width="711" height="149" alt="image" src="https://github.com/user-attachments/assets/a29e4c8c-cf27-4bc2-8bd3-11a3ff066050" />

> - Subdomain Findings
<img width="530" height="124" alt="image" src="https://github.com/user-attachments/assets/39ee5cdb-c9c9-4968-a72d-5ddd864a5046" />

---

## ⚙️ Setup (Using Virtual Environment)

```bash
# Clone domain_threathunter.py & requirements.txt
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

# Insert your VirusTotal API key
# (Open the script and replace the placeholder value with your VT API key)
api_key = "your_api_key_here"

# Usage
python3 domain_threathunter.py <domain>
