import subprocess

def toggle_warp(enabled: bool):
    action = enabled and "connect" or "disconnect"
    try:
        result = subprocess.run(["warp-cli", action], check=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return e
    