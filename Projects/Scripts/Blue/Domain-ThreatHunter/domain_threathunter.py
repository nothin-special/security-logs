import socket
import ssl
import requests
import whois
import dns.resolver
import dns.reversename
import shodan
import virustotal_python
from ipwhois import IPWhois
from datetime import datetime, timezone

# WHOIS Lookup
def whois_lookup(domain):
    try:
        whois_information = whois.whois(domain)

        # Function to format date
        def format_date(date):
            if isinstance(date, list):
                return [d.strftime('%Y-%m-%d %H:%M:%S') if isinstance(d, datetime) else d for d in date]
            elif isinstance(date, datetime):
                return date.strftime('%Y-%m-%d %H:%M:%S')
            return date

        print("\n\033[0;32mDomain Name:", whois_information.domain_name)
        print("Domain registrar:", whois_information.registrar)
        print("WHOis server:", whois_information.whois_server)
        print("Domain creation date:", format_date(whois_information.creation_date))
        print("Expiration date:", format_date(whois_information.expiration_date))
        print("Updated Date:", format_date(whois_information.updated_date))
        print("Servers:", whois_information.name_servers)
        print("Status:", whois_information.status)
        print("Email Addresses:", whois_information.emails)
        print("Name:", whois_information.name)
        print("Org:", whois_information.org)
        print("Address:", whois_information.address)
        print("City:", whois_information.city)
        print("State:", whois_information.state)
        print("Zipcode:", whois_information.zipcode)
        print("Country:", whois_information.country)
    except Exception as e:
        print(f"Error performing WHOIS lookup: {e}")
        return None

# DNS Records Lookup
def dns_lookup(domain):
    records = {}
    try:
        answers = dns.resolver.resolve(domain, 'A')
        records['A'] = [answer.to_text() for answer in answers]
    except Exception as e:
        print(f"Error gathering A records: {e}")
        records['A'] = None

    try:
        answers = dns.resolver.resolve(domain, 'NS')
        records['NS'] = [answer.to_text() for answer in answers]
    except Exception as e:
        print(f"Error gathering NS records: {e}")
        records['NS'] = None

    try:
        answers = dns.resolver.resolve(domain, 'MX')
        records['MX'] = [answer.to_text() for answer in answers]
    except Exception as e:
        print(f"Error gathering MX records: {e}")
        records['MX'] = None

    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        records['TXT'] = [answer.to_text() for answer in answers]
    except Exception as e:
        print(f"Error gathering TXT records: {e}")
        records['TXT'] = None

    try:
        answers = dns.resolver.resolve(domain, 'SOA')
        records['SOA'] = [answer.to_text() for answer in answers]
    except Exception as e:
        print(f"Error gathering SOA records: {e}")
        records['SOA'] = None
    try:
        answers = dns.resolver.resolve(domain, 'CNAME')
        records['CNAME'] = [answer.to_text() for answer in answers]
    except Exception as e:
        print(f"Error gathering CNAME records: {e}")
        records['CNAME'] = None
    return records

# SSL/TLS Certificate Information
def get_ssl_info(domain, timeout=20):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                ssl_info = {
                    'subject': dict(x[0] for x in cert['subject']),
                    'issuer': dict(x[0] for x in cert['issuer']),
                    'serialNumber': cert.get('serialNumber'),
                    'version': cert.get('version'),
                    'notBefore': cert.get('notBefore'),
                    'notAfter': cert.get('notAfter'),
                    'subjectAltName': cert.get('subjectAltName')
                }
                return ssl_info
    except Exception as e:
        print(f"Error parsing SSL/TLS certificate information: {e}")
        return None

# Reverse DNS Lookup
def reverse_dns_lookup(ip_address):
    try:
        rev_name = dns.reversename.from_address(ip_address)
        reversed_dns = str(dns.resolver.resolve(rev_name, "PTR")[0])
        return reversed_dns
    except Exception as e:
        print(f"Error performing reverse DNS lookup for {ip_address}: {e}")
        return None

# ASN and Geolocation Lookup
def asn_lookup(ip_address):
    try:
        obj = IPWhois(ip_address)
        result = obj.lookup_rdap()
        asn_info = {
            'ASN': result.get('asn'),
            'ASN Country Code': result.get('asn_country_code'),
            'ASN Description': result.get('asn_description'),
            'ASN CIDR': result.get('asn_cidr'),
            'ASN Date': result.get('asn_date')
        }
        return asn_info
    except Exception as e:
        print(f"Error performing ASN lookup for {ip_address}: {e}")
        return None

# VirusTotal Check (final fixed version)
def check_virustotal(url):
    import base64
    try:
        api_key = "REMOVED"

        # Encode the URL to base64 ID format (VT requirement)
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")

        with virustotal_python.Virustotal(API_KEY=api_key) as vtotal:
            response = vtotal.request(f"urls/{url_id}", method="GET").json()
            attributes = response["data"]["attributes"]
            stats = attributes["last_analysis_stats"]

            permalink = f"https://www.virustotal.com/gui/url/{url_id}/detection"

            return {
                'positives': stats.get('malicious', 0),
                'permalink': permalink,
                'scan_date': datetime.fromtimestamp(attributes["last_analysis_date"], timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            }
    except Exception as e:
        print(f"Error checking VirusTotal: {e}")
        return None

# Web Technology Fingerprinting
def web_technology_fingerprint(url):
    try:
        response = requests.get(url)
        if 'server' in response.headers:
            return response.headers['server']
        else:
            return 'Unknown'
    except Exception as e:
        print(f"Error gathering web technology fingerprint: {e}")
        return 'Unknown'

def subdomain_scanner(domain):
    subdomains_found = []
    sdsreq = requests.get(f'https://crt.sh/?q={domain}&output=json')
    if sdsreq.status_code == 200:
        print("\033[0;32mEnumerating Subdomains...\033[0m")
    else:
        print("\033[0;32mThe subdomain scanner tool is currently offline, please try again in a few minutes!\033[0m")
        sys.exit(1)

    for (key, value) in enumerate(sdsreq.json()):
        subdomains_found.append(value['name_value'])

    print(
        f"\n\n\033[0;35m\033[1mYour chosen targeted Domain for the Subdomain scan:\033[0;32m{domain}\033[0m\033[0;32m\n")

    subdomains = sorted(set(subdomains_found))

    for sub_link in subdomains:
        print(f'\033[1m[Subdomain Found]\033[0m\033[0;32m -->{sub_link}')

    print("\n\033[1m\033[0;35m\033[1mSubdomain Scan Completed!  \033[0;32m\033[1m- ALL Subdomains have been Found")

# Main function to perform domain analysis
def domain_analysis(domain):
    print(f"Summary for {domain}:")

    # WHOIS Information
    whois_info = whois_lookup(domain)
    if whois_info:
        print("\n[WHOIS Information]")
        print(whois_info)

    # DNS Information
    dns_info = dns_lookup(domain)
    print("\n[DNS Information]")
    for record_type, records in dns_info.items():
        print(f"{record_type} Records: {records}")

    # SSL/TLS Certificate Information
    ssl_info = get_ssl_info(domain)
    if ssl_info:
        print("\n[SSL/TLS Certificate Information]")
        for key, value in ssl_info.items():
            print(f"{key}: {value}")

    # Reverse DNS Lookup
    print("\n[Reverse DNS Lookup]")
    for ip in dns_info.get('A', []):
        rdns = reverse_dns_lookup(ip)
        print(f"Reverse DNS for {ip}: {rdns}")

    # ASN and Geolocation Information
    print("\n[ASN and Geolocation]")
    for ip in dns_info.get('A', []):
        asn_info = asn_lookup(ip)
        if asn_info:
            print(f"ASN and Geolocation for {ip}: {asn_info}")

    # Web Technology Fingerprinting
    print("\n[Web Technology Fingerprinting]")
    web_tech = web_technology_fingerprint(f"http://{domain}")
    print(f"Web Server Technology: {web_tech}")

    # Blacklist Checks
    print("\n[Blacklist Checks]")
    vt_info = check_virustotal(f"http://{domain}")
    if vt_info:
        print("VirusTotal:")
        print(f" - Scan Date: {vt_info['scan_date']}")
        print(f" - Positives: {vt_info['positives']}")
        print(f" - Permalink: {vt_info['permalink']}")

    #Subdomain Check through crt.sh
    print("\n[Passive Subdomain Enumeration]")
    subdomains = subdomain_scanner(domain)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <domain>")
    else:
        domain = sys.argv[1]
        domain_analysis(domain)
