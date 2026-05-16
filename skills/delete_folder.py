import os
import shutil

def delete_folder(folder_path: str) -> dict:
    """
    Deletes the specified folder and all its contents.

    Args:
        folder_path: The path to the folder to be deleted.

    Returns:
        dict with keys: success (bool), path (str), message (str)
    """
    if not folder_path or not folder_path.strip():
        return {"success": False, "path": folder_path, "message": "Folder path cannot be empty."}

    folder_path = os.path.expanduser(folder_path.strip())

    if not os.path.exists(folder_path):
        return {"success": False, "path": folder_path, "message": f"Folder '{folder_path}' does not exist."}

    if not os.path.isdir(folder_path):
        return {"success": False, "path": folder_path, "message": f"'{folder_path}' is a file, not a folder."}

    try:
        shutil.rmtree(folder_path)
        return {"success": True, "path": folder_path, "message": f"Folder '{folder_path}' deleted successfully."}
    except PermissionError:
        return {"success": False, "path": folder_path, "message": f"Permission denied: cannot delete '{folder_path}'."}
    except Exception as e:
        return {"success": False, "path": folder_path, "message": f"Unexpected error: {e}"}