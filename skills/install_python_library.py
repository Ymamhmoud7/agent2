import subprocess
import sys

def install_python_library(library_name: str) -> dict:
    """
    Install a Python library using pip.

    Args:
        library_name: Name of the library to install (e.g. "requests" or "requests==2.28.0").

    Returns:
        dict with keys: success (bool), library (str), message (str)
    """
    if not library_name or not library_name.strip():
        return {"success": False, "library": library_name, "message": "Library name cannot be empty."}

    library_name = library_name.strip()

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", library_name],
            check=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        output = result.stdout.strip().splitlines()
        # Last meaningful line is usually "Successfully installed X"
        summary = next((l for l in reversed(output) if l.strip()), "Installed successfully.")
        return {"success": True, "library": library_name, "message": summary}

    except subprocess.TimeoutExpired:
        return {"success": False, "library": library_name, "message": "pip install timed out after 120 seconds."}
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.strip() if e.stderr else "Unknown error"
        return {"success": False, "library": library_name, "message": f"pip install failed: {stderr}"}
    except Exception as e:
        return {"success": False, "library": library_name, "message": f"Unexpected error: {e}"}