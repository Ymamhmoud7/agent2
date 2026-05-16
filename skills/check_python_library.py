import subprocess
import sys
import json

DESCRIPTION = "Check if a Python library is installed, or list all installed libraries."

EXAMPLES = [
    {
        "user": "is requests installed?",
        "plan": [
            {
                "type": "call",
                "function": "check_python_library",
                "args": {
                    "library_name": "requests"
                }
            }
        ]
    },
    {
        "user": "check if numpy is available",
        "plan": [
            {
                "type": "call",
                "function": "check_python_library",
                "args": {
                    "library_name": "numpy"
                }
            }
        ]
    },
    {
        "user": "list all installed python libraries",
        "plan": [
            {
                "type": "call",
                "function": "list_python_libraries",
                "args": {}
            }
        ]
    }
]



def check_python_library(library_name: str) -> dict:
    """
    Check whether a Python library is installed and get its version.

    Args:
        library_name: Name of the library to check.

    Returns:
        dict with keys: success (bool), library (str), installed (bool), version (str|None), message (str)
    """
    if not library_name or not library_name.strip():
        return {"success": False, "library": library_name, "installed": False, "version": None, "message": "Library name cannot be empty."}

    library_name = library_name.strip()

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", library_name],
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode == 0:
            version = None
            for line in result.stdout.splitlines():
                if line.startswith("Version:"):
                    version = line.split(":", 1)[1].strip()
                    break
            return {"success": True, "library": library_name, "installed": True, "version": version, "message": f"{library_name} is installed (version {version})."}
        else:
            return {"success": True, "library": library_name, "installed": False, "version": None, "message": f"{library_name} is not installed."}

    except subprocess.TimeoutExpired:
        return {"success": False, "library": library_name, "installed": False, "version": None, "message": "pip show timed out."}
    except Exception as e:
        return {"success": False, "library": library_name, "installed": False, "version": None, "message": f"Unexpected error: {e}"}


def list_python_libraries() -> dict:
    """
    List all installed Python libraries with their versions.

    Returns:
        dict with keys: success (bool), libraries (list of {name, version}), message (str)
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            libraries = json.loads(result.stdout)
            return {"success": True, "libraries": libraries, "message": f"{len(libraries)} libraries installed."}
        else:
            return {"success": False, "libraries": [], "message": "pip list failed."}

    except subprocess.TimeoutExpired:
        return {"success": False, "libraries": [], "message": "pip list timed out."}
    except Exception as e:
        return {"success": False, "libraries": [], "message": f"Unexpected error: {e}"}