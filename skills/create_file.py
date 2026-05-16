import os


def create_file(file_path: str, content: str = "", overwrite: bool = False) -> dict:
    """
    Create a new file at the given path, optionally with content.

    Args:
        file_path: Full path where the file should be created (e.g. "~/notes/todo.txt").
        content:   Text to write into the file. Defaults to empty string.
        overwrite: If True, overwrite the file if it already exists. Defaults to False.

    Returns:
        dict with keys: success (bool), file_path (str), message (str)
    """
    if not file_path or not file_path.strip():
        return {"success": False, "file_path": file_path, "message": "File path cannot be empty."}

    file_path = os.path.expanduser(file_path.strip())

    if os.path.isdir(file_path):
        return {"success": False, "file_path": file_path, "message": f"'{file_path}' is an existing directory, not a file."}

    if os.path.exists(file_path) and not overwrite:
        return {"success": False, "file_path": file_path, "message": f"File '{file_path}' already exists. Set overwrite=True to replace it."}

    parent_dir = os.path.dirname(os.path.abspath(file_path))

    try:
        os.makedirs(parent_dir, exist_ok=True)
    except PermissionError:
        return {"success": False, "file_path": file_path, "message": f"Permission denied: cannot create directory '{parent_dir}'."}
    except Exception as e:
        return {"success": False, "file_path": file_path, "message": f"Failed to create parent directory: {e}"}

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        action = "overwritten" if os.path.exists(file_path) else "created"
        return {"success": True, "file_path": file_path, "message": f"File '{file_path}' {action} successfully."}
    except PermissionError:
        return {"success": False, "file_path": file_path, "message": f"Permission denied: cannot write to '{file_path}'."}
    except Exception as e:
        return {"success": False, "file_path": file_path, "message": f"Unexpected error: {e}"}