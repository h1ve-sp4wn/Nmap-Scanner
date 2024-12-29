import socket
import requests
import nmap
import asyncio
import struct
from time import sleep
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def advanced_stealth_port_scanner(ip):
    try:
        scanner = nmap.PortScanner()
        scan_arguments = '-sS -p 1-65535 -T2 -f -D RND:10 --randomize-hosts -Pn --spoof-mac 00:11:22:33:44:55'
        scanner.scan(ip, arguments=scan_arguments)

        open_ports = []
        if 'tcp' in scanner[ip]:
            for port in scanner[ip]['tcp']:
                if scanner[ip]['tcp'][port]['state'] == 'open':
                    open_ports.append(port)
        return open_ports
    except Exception as e:
        print(f"Error during scanning: {e}")
        return []

async def check_service_versions(ip, ports):
    services = {}

    async def get_banner(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip, port))
            banner = sock.recv(1024).decode(errors="ignore").strip()
            sock.close()
            return port, banner
        except Exception as e:
            return port, f"Error: {e}"

    tasks = [get_banner(port) for port in ports]
    results = await asyncio.gather(*tasks)

    for port, banner in results:
        services[port] = banner
    return services

def check_memory_vulnerabilities(ip, ports):
    vulnerabilities = []

    def detect_overflow(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip, port))

            payload = b"A" * 2048  # Typically large enough to cause overflow
            sock.send(payload)

            response = sock.recv(1024)
            sock.close()

            if not response or len(response) < 10:
                vulnerabilities.append(f"Potential buffer overflow detected on port {port}")
        except Exception:
            vulnerabilities.append(f"Error during overflow test on port {port}")
    
    for port in ports:
        detect_overflow(port)

    return vulnerabilities

def check_web_vulnerabilities(url):
    vulnerabilities = []
    
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.mount("https://", HTTPAdapter(max_retries=retries))
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = session.get(url, headers=headers)
        
        security_headers = response.headers
        if 'X-Content-Type-Options' not in security_headers:
            vulnerabilities.append("Missing X-Content-Type-Options")
        if 'X-Frame-Options' not in security_headers:
            vulnerabilities.append("Missing X-Frame-Options")
        if 'Strict-Transport-Security' not in security_headers:
            vulnerabilities.append("Missing Strict-Transport-Security")
    except requests.RequestException as e:
        vulnerabilities.append(f"Error accessing URL: {e}")
    
    return vulnerabilities

async def vulnerability_scanner(ip, url):
    print(f"Starting advanced stealth scan on {ip}...")
    open_ports = advanced_stealth_port_scanner(ip)
    print(f"Open ports found: {open_ports}")

    print("\nChecking service versions asynchronously...")
    service_versions = await check_service_versions(ip, open_ports)
    for port, version in service_versions.items():
        print(f"Port {port}: {version}")

    print("\nChecking for potential memory vulnerabilities...")
    memory_vulns = check_memory_vulnerabilities(ip, open_ports)
    for vuln in memory_vulns:
        print(f"Memory Vulnerability: {vuln}")

    print("\nChecking web vulnerabilities...")
    web_vulns = check_web_vulnerabilities(url)
    for vuln in web_vulns:
        print(f"Vulnerability: {vuln}")

ip_address = "192.168.1.1"  # Replace with target IP
url = "http://example.com"  # Replace with target URL

asyncio.run(vulnerability_scanner(ip_address, url))