import os
import shutil

DESCRIPTION = "Move a folder into a different parent directory."

EXAMPLES = [
    {
        "user": "move ~/projects/old_project to ~/archive",
        "plan": [
            {
                "type": "call",
                "function": "move_folder",
                "args": {
                    "folder_path": "~/projects/old_project",
                    "destination_dir": "~/archive"
                }
            }
        ]
    }
]




def move_folder(folder_path: str, destination_dir: str, overwrite: bool = False) -> dict:
    """
    Move a folder into a different parent directory.

    Args:
        folder_path:     Path to the folder to move (e.g. "~/projects/old_project").
        destination_dir: Path to the target parent directory (e.g. "~/archive").
        overwrite:       If True, overwrite the destination folder if one with the same
                         name already exists there. Defaults to False.

    Returns:
        dict with keys: success (bool), old_path (str), new_path (str), message (str)
    """
    if not folder_path or not folder_path.strip():
        return {"success": False, "old_path": folder_path, "new_path": None, "message": "Folder path cannot be empty."}

    if not destination_dir or not destination_dir.strip():
        return {"success": False, "old_path": folder_path, "new_path": None, "message": "Destination directory cannot be empty."}

    folder_path = os.path.expanduser(folder_path.strip())
    destination_dir = os.path.expanduser(destination_dir.strip())

    if not os.path.exists(folder_path):
        return {"success": False, "old_path": folder_path, "new_path": None, "message": f"Folder '{folder_path}' does not exist."}

    if not os.path.isdir(folder_path):
        return {"success": False, "old_path": folder_path, "new_path": None, "message": f"'{folder_path}' is a file, not a folder. Use move_file instead."}

    if os.path.exists(destination_dir) and not os.path.isdir(destination_dir):
        return {"success": False, "old_path": folder_path, "new_path": None, "message": f"'{destination_dir}' exists but is not a directory."}

    # Prevent moving a folder into itself or a subdirectory of itself
    abs_src = os.path.abspath(folder_path)
    abs_dst = os.path.abspath(destination_dir)
    if abs_dst.startswith(abs_src + os.sep) or abs_dst == abs_src:
        return {"success": False, "old_path": folder_path, "new_path": None, "message": "Cannot move a folder into itself or one of its subfolders."}

    folder_name = os.path.basename(abs_src)
    new_path = os.path.join(destination_dir, folder_name)

    if os.path.exists(new_path) and not overwrite:
        return {"success": False, "old_path": folder_path, "new_path": new_path, "message": f"A folder named '{folder_name}' already exists in '{destination_dir}'. Set overwrite=True to replace it."}

    try:
        os.makedirs(destination_dir, exist_ok=True)
        if overwrite and os.path.exists(new_path):
            shutil.rmtree(new_path)
        shutil.move(folder_path, new_path)
        return {"success": True, "old_path": folder_path, "new_path": new_path, "message": f"Folder moved from '{folder_path}' to '{new_path}'."}
    except PermissionError:
        return {"success": False, "old_path": folder_path, "new_path": new_path, "message": f"Permission denied: cannot move '{folder_path}'."}
    except Exception as e:
        return {"success": False, "old_path": folder_path, "new_path": None, "message": f"Unexpected error: {e}"}