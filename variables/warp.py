import requests

def is_warp_connected():
    try:
        response = requests.get('https://www.cloudflare.com/cdn-cgi/trace')
        if response.status_code == 200:
            return 'warp=on' in response.text or 'warp=plus' in response.text
        return False
    except requests.RequestException:
        return False
    
def get_warp_status():
    if is_warp_connected():
        return "Connected to Cloudflare WARP"
    else:
        return "Not connected to Cloudflare WARP"