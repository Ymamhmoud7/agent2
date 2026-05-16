import os


def edit_file(file_path: str, old_text: str, new_text: str) -> dict:
    """
    Replace the first occurrence of a string in a file with new text.

    Args:
        file_path: Path to the file to edit (e.g. "~/notes/todo.txt").
        old_text:  The exact string to search for and replace.
        new_text:  The string to substitute in place of old_text.

    Returns:
        dict with keys: success (bool), file_path (str), replacements (int), message (str)
    """
    if not file_path or not file_path.strip():
        return {"success": False, "file_path": file_path, "replacements": 0, "message": "File path cannot be empty."}

    if old_text is None:
        return {"success": False, "file_path": file_path, "replacements": 0, "message": "old_text cannot be None."}

    file_path = os.path.expanduser(file_path.strip())

    if not os.path.exists(file_path):
        return {"success": False, "file_path": file_path, "replacements": 0, "message": f"File '{file_path}' does not exist."}

    if os.path.isdir(file_path):
        return {"success": False, "file_path": file_path, "replacements": 0, "message": f"'{file_path}' is a directory, not a file."}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original = f.read()
    except UnicodeDecodeError:
        return {"success": False, "file_path": file_path, "replacements": 0, "message": f"'{file_path}' does not appear to be a UTF-8 text file."}
    except PermissionError:
        return {"success": False, "file_path": file_path, "replacements": 0, "message": f"Permission denied: cannot read '{file_path}'."}
    except Exception as e:
        return {"success": False, "file_path": file_path, "replacements": 0, "message": f"Unexpected error reading file: {e}"}

    count = original.count(old_text)
    if count == 0:
        return {"success": False, "file_path": file_path, "replacements": 0, "message": "old_text was not found in the file. No changes made."}

    updated = original.replace(old_text, new_text)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated)
        return {"success": True, "file_path": file_path, "replacements": count, "message": f"Replaced {count} occurrence(s) of old_text in '{file_path}'."}
    except PermissionError:
        return {"success": False, "file_path": file_path, "replacements": 0, "message": f"Permission denied: cannot write to '{file_path}'."}
    except Exception as e:
        return {"success": False, "file_path": file_path, "replacements": 0, "message": f"Unexpected error writing file: {e}"}