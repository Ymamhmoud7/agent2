import platform
import os
import shutil


def get_system_info() -> dict:
    """
    Return a snapshot of key system information.

    Returns:
        dict with keys: success (bool), os (str), os_version (str), architecture (str),
                        hostname (str), cpu_count (int|None), disk (dict), message (str)

        disk dict keys: total_gb (float), used_gb (float), free_gb (float), percent_used (float)
    """
    try:
        uname = platform.uname()

        # Disk usage for the root/home partition
        disk_path = os.path.expanduser("~")
        disk = shutil.disk_usage(disk_path)

        def to_gb(b):
            return round(b / (1024 ** 3), 2)

        disk_info = {
            "total_gb": to_gb(disk.total),
            "used_gb": to_gb(disk.used),
            "free_gb": to_gb(disk.free),
            "percent_used": round((disk.used / disk.total) * 100, 1)
        }

        return {
            "success": True,
            "os": uname.system,
            "os_version": uname.version,
            "architecture": uname.machine,
            "hostname": uname.node,
            "cpu_count": os.cpu_count(),
            "disk": disk_info,
            "message": f"System info retrieved: {uname.system} {uname.machine}, {disk_info['free_gb']} GB free."
        }

    except Exception as e:
        return {
            "success": False,
            "os": None,
            "os_version": None,
            "architecture": None,
            "hostname": None,
            "cpu_count": None,
            "disk": None,
            "message": f"Unexpected error: {e}"
        }