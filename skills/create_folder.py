import os

def create_folder(folder_name: str, parent_path: str = ".") -> dict:
    """
    Create a new folder with the given name.
    
    Args:
        folder_name: Name of the folder to create.
        parent_path: Where to create it. Defaults to current directory.
    
    Returns:
        dict with keys: success (bool), path (str), message (str)
    """
    if not folder_name or not folder_name.strip():
        return {"success": False, "path": None, "message": "Folder name cannot be empty."}

    # Sanitize: strip leading/trailing spaces and reject path traversal
    folder_name = folder_name.strip()
    if any(c in folder_name for c in ("/", "\\", "..")):
        return {"success": False, "path": None, "message": f"Invalid folder name: '{folder_name}'."}

    full_path = os.path.join(parent_path, folder_name)

    try:
        if os.path.exists(full_path):
            return {"success": True, "path": full_path, "message": f"Folder '{full_path}' already exists."}
        
        os.makedirs(full_path, exist_ok=True)
        return {"success": True, "path": full_path, "message": f"Folder '{full_path}' created successfully."}
    
    except PermissionError:
        return {"success": False, "path": None, "message": f"Permission denied: cannot create '{full_path}'."}
    except OSError as e:
        return {"success": False, "path": None, "message": f"OS error: {e}"}