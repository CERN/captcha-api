import urllib.request
import os

starfleetipdefender = os.environ.get("STARFLEETIPDEFENDER", default="https://starfleetipdefender.prod.padam.io")

def is_ip_blacklisted(ip):
    
    url = f"{starfleetipdefender}/blacklisted-ip/{ip}/"
    try:
        response = urllib.request.urlopen(url)
        response_code = response.getcode()
        return response_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False