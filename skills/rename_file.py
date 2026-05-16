import os


def rename_file(file_path: str, new_name: str) -> dict:
    """
    Rename a file while keeping it in the same parent directory.

    Args:
        file_path: Path to the file to rename (e.g. "~/docs/old_name.txt").
        new_name:  The new name for the file, not a full path (e.g. "new_name.txt").

    Returns:
        dict with keys: success (bool), old_path (str), new_path (str), message (str)
    """
    if not file_path or not file_path.strip():
        return {"success": False, "old_path": file_path, "new_path": None, "message": "File path cannot be empty."}

    if not new_name or not new_name.strip():
        return {"success": False, "old_path": file_path, "new_path": None, "message": "New name cannot be empty."}

    file_path = os.path.expanduser(file_path.strip())
    new_name = new_name.strip()

    if any(c in new_name for c in ("/", "\\", "..")):
        return {"success": False, "old_path": file_path, "new_path": None, "message": f"Invalid file name: '{new_name}'. Use a name, not a path."}

    if not os.path.exists(file_path):
        return {"success": False, "old_path": file_path, "new_path": None, "message": f"File '{file_path}' does not exist."}

    if os.path.isdir(file_path):
        return {"success": False, "old_path": file_path, "new_path": None, "message": f"'{file_path}' is a directory, not a file. Use rename_folder instead."}

    parent = os.path.dirname(os.path.abspath(file_path))
    new_path = os.path.join(parent, new_name)

    if os.path.exists(new_path):
        return {"success": False, "old_path": file_path, "new_path": new_path, "message": f"A file named '{new_name}' already exists in the same directory."}

    try:
        os.rename(file_path, new_path)
        return {"success": True, "old_path": file_path, "new_path": new_path, "message": f"File renamed from '{file_path}' to '{new_path}'."}
    except PermissionError:
        return {"success": False, "old_path": file_path, "new_path": new_path, "message": f"Permission denied: cannot rename '{file_path}'."}
    except Exception as e:
        return {"success": False, "old_path": file_path, "new_path": None, "message": f"Unexpected error: {e}"}