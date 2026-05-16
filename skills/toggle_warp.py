import subprocess

def toggle_warp(enabled: bool) -> dict:
    """
    Connect or disconnect Cloudflare WARP.

    Args:
        enabled: True to connect, False to disconnect.

    Returns:
        dict with keys: success (bool), action (str), message (str)
    """
    action = "connect" if enabled else "disconnect"

    try:
        result = subprocess.run(
            ["warp-cli", action],
            check=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout.strip() or f"WARP {action}ed successfully."
        return {"success": True, "action": action, "message": output}

    except FileNotFoundError:
        return {"success": False, "action": action, "message": "warp-cli not found. Is Cloudflare WARP installed?"}
    except subprocess.TimeoutExpired:
        return {"success": False, "action": action, "message": f"warp-cli {action} timed out after 10 seconds."}
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.strip() if e.stderr else "Unknown error"
        return {"success": False, "action": action, "message": f"warp-cli {action} failed: {stderr}"}
    except Exception as e:
        return {"success": False, "action": action, "message": f"Unexpected error: {e}"}