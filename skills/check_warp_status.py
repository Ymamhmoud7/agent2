import subprocess
import sys

DESCRIPTION = "Check whether Cloudflare WARP is currently connected or disconnected."

EXAMPLES = [
    {
        "user": "is warp on?",
        "plan": [
            {
                "type": "call",
                "function": "check_warp_status",
                "args": {}
            }
        ]
    },
    {
        "user": "what is the warp status?",
        "plan": [
            {
                "type": "call",
                "function": "check_warp_status",
                "args": {}
            }
        ]
    }
]



def check_warp_status() -> dict:
    """
    Check whether Cloudflare WARP is currently connected or disconnected.

    Returns:
        dict with keys: success (bool), connected (bool), status (str), message (str)
    """
    try:
        result = subprocess.run(
            ["warp-cli", "status"],
            capture_output=True,
            text=True,
            timeout=10
        )

        output = result.stdout.strip().lower()

        if "connected" in output and "disconnected" not in output:
            return {"success": True, "connected": True, "status": "connected", "message": "WARP is currently connected."}
        elif "disconnected" in output:
            return {"success": True, "connected": False, "status": "disconnected", "message": "WARP is currently disconnected."}
        else:
            return {"success": True, "connected": None, "status": "unknown", "message": f"WARP status unclear: {result.stdout.strip()}"}

    except FileNotFoundError:
        return {"success": False, "connected": None, "status": "error", "message": "warp-cli not found. Is Cloudflare WARP installed?"}
    except subprocess.TimeoutExpired:
        return {"success": False, "connected": None, "status": "error", "message": "warp-cli status timed out."}
    except Exception as e:
        return {"success": False, "connected": None, "status": "error", "message": f"Unexpected error: {e}"}