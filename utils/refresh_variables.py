import json
import os

from skills.get_system_info import get_system_info
from variables.warp import get_warp_status
from variables.location import get_current_location
from variables.time import return_time
from datetime import datetime

VARIABLES_DIR = os.path.join(os.path.dirname(__file__), "variables")
os.makedirs(VARIABLES_DIR, exist_ok=True)


def _write(name: str, value):
    path = os.path.join(VARIABLES_DIR, f"{name}.json")
    payload = {
        "value": value,
        "refreshed_at": datetime.now().isoformat()
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"[variables] ✓ {name}")


# ── Refreshers ────────────────────────────────────────────────────────────────

def refresh_time():
    _write("time", return_time())


def refresh_location():
    try:
        _write("location", get_current_location())
    except Exception as e:
        _write("location", f"unavailable ({e})")


def refresh_warp_status():
    try:
        _write("warp_status", get_warp_status())
    except Exception as e:
        _write("warp_status", f"unavailable ({e})")


def refresh_system_info():
    try:
        info = get_system_info()
        summary = {
            "os":           info.get("os"),
            "architecture": info.get("architecture"),
            "hostname":     info.get("hostname"),
            "cpu_count":    info.get("cpu_count"),
            "disk":         info.get("disk"),
        }
        _write("system_info", summary)
    except Exception as e:
        _write("system_info", f"unavailable ({e})")


REFRESHERS = [
    refresh_time,
    refresh_location,
    refresh_warp_status,
    refresh_system_info,
]


def refresh_all():
    print("[variables] Refreshing live variables...")
    for fn in REFRESHERS:
        try:
            fn()
        except Exception as e:
            print(f"[variables] ✗ {fn.__name__}: {e}")
    print("[variables] Done.")


if __name__ == "__main__":
    refresh_all()