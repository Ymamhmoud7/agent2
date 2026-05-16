import os

DESCRIPTION = "Delete a file at a given path."

EXAMPLES = [
    {
        "user": "delete ~/downloads/old_report.pdf",
        "plan": [
            {
                "type": "call",
                "function": "delete_file",
                "args": {
                    "file_path": "~/downloads/old_report.pdf"
                }
            }
        ]
    }
]




def delete_file(file_path: str) -> dict:
    """
    Delete a file at the given path.

    Args:
        file_path: Path to the file to delete (e.g. "~/notes/todo.txt").

    Returns:
        dict with keys: success (bool), file_path (str), message (str)
    """
    if not file_path or not file_path.strip():
        return {"success": False, "file_path": file_path, "message": "File path cannot be empty."}

    file_path = os.path.expanduser(file_path.strip())

    if not os.path.exists(file_path):
        return {"success": False, "file_path": file_path, "message": f"File '{file_path}' does not exist."}

    if os.path.isdir(file_path):
        return {"success": False, "file_path": file_path, "message": f"'{file_path}' is a directory, not a file. Use delete_folder instead."}

    try:
        os.remove(file_path)
        return {"success": True, "file_path": file_path, "message": f"File '{file_path}' deleted successfully."}
    except PermissionError:
        return {"success": False, "file_path": file_path, "message": f"Permission denied: cannot delete '{file_path}'."}
    except Exception as e:
        return {"success": False, "file_path": file_path, "message": f"Unexpected error: {e}"}