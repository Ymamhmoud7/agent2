import os

def rename_folder(folder_path: str, new_name: str) -> dict:
    """
    Rename a folder while keeping it in the same parent directory.

    Args:
        folder_path: Path to the folder to rename.
        new_name: The new name for the folder (not a full path, just the name).

    Returns:
        dict with keys: success (bool), old_path (str), new_path (str), message (str)
    """
    if not folder_path or not folder_path.strip():
        return {"success": False, "old_path": folder_path, "new_path": None, "message": "Folder path cannot be empty."}

    if not new_name or not new_name.strip():
        return {"success": False, "old_path": folder_path, "new_path": None, "message": "New name cannot be empty."}

    folder_path = os.path.expanduser(folder_path.strip())
    new_name = new_name.strip()

    if any(c in new_name for c in ("/", "\\", "..")):
        return {"success": False, "old_path": folder_path, "new_path": None, "message": f"Invalid folder name: '{new_name}'. Use a name, not a path."}

    if not os.path.exists(folder_path):
        return {"success": False, "old_path": folder_path, "new_path": None, "message": f"Folder '{folder_path}' does not exist."}

    if not os.path.isdir(folder_path):
        return {"success": False, "old_path": folder_path, "new_path": None, "message": f"'{folder_path}' is a file, not a folder."}

    parent = os.path.dirname(os.path.abspath(folder_path))
    new_path = os.path.join(parent, new_name)

    if os.path.exists(new_path):
        return {"success": False, "old_path": folder_path, "new_path": new_path, "message": f"A folder named '{new_name}' already exists in the same directory."}

    try:
        os.rename(folder_path, new_path)
        return {"success": True, "old_path": folder_path, "new_path": new_path, "message": f"Folder renamed from '{folder_path}' to '{new_path}'."}
    except PermissionError:
        return {"success": False, "old_path": folder_path, "new_path": new_path, "message": f"Permission denied: cannot rename '{folder_path}'."}
    except Exception as e:
        return {"success": False, "old_path": folder_path, "new_path": None, "message": f"Unexpected error: {e}"}