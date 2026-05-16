import os
import shutil


def move_file(file_path: str, destination_dir: str, overwrite: bool = False) -> dict:
    """
    Move a file to a different directory.

    Args:
        file_path:       Path to the file to move (e.g. "~/downloads/report.pdf").
        destination_dir: Path to the target directory (e.g. "~/docs/reports").
        overwrite:       If True, overwrite the file if one with the same name exists
                         in the destination. Defaults to False.

    Returns:
        dict with keys: success (bool), old_path (str), new_path (str), message (str)
    """
    if not file_path or not file_path.strip():
        return {"success": False, "old_path": file_path, "new_path": None, "message": "File path cannot be empty."}

    if not destination_dir or not destination_dir.strip():
        return {"success": False, "old_path": file_path, "new_path": None, "message": "Destination directory cannot be empty."}

    file_path = os.path.expanduser(file_path.strip())
    destination_dir = os.path.expanduser(destination_dir.strip())

    if not os.path.exists(file_path):
        return {"success": False, "old_path": file_path, "new_path": None, "message": f"File '{file_path}' does not exist."}

    if os.path.isdir(file_path):
        return {"success": False, "old_path": file_path, "new_path": None, "message": f"'{file_path}' is a directory, not a file. Use move_folder instead."}

    if os.path.exists(destination_dir) and not os.path.isdir(destination_dir):
        return {"success": False, "old_path": file_path, "new_path": None, "message": f"'{destination_dir}' exists but is not a directory."}

    file_name = os.path.basename(file_path)
    new_path = os.path.join(destination_dir, file_name)

    if os.path.exists(new_path) and not overwrite:
        return {"success": False, "old_path": file_path, "new_path": new_path, "message": f"'{file_name}' already exists in '{destination_dir}'. Set overwrite=True to replace it."}

    try:
        os.makedirs(destination_dir, exist_ok=True)
        shutil.move(file_path, new_path)
        return {"success": True, "old_path": file_path, "new_path": new_path, "message": f"File moved from '{file_path}' to '{new_path}'."}
    except PermissionError:
        return {"success": False, "old_path": file_path, "new_path": new_path, "message": f"Permission denied: cannot move '{file_path}'."}
    except Exception as e:
        return {"success": False, "old_path": file_path, "new_path": None, "message": f"Unexpected error: {e}"}