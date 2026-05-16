import os


def read_file(file_path: str, encoding: str = "utf-8") -> dict:
    """
    Read and return the contents of a text file.

    Args:
        file_path: Path to the file to read (e.g. "~/notes/todo.txt").
        encoding:  File encoding. Defaults to "utf-8".

    Returns:
        dict with keys: success (bool), file_path (str), content (str|None),
                        size_bytes (int|None), line_count (int|None), message (str)
    """
    if not file_path or not file_path.strip():
        return {"success": False, "file_path": file_path, "content": None, "size_bytes": None, "line_count": None, "message": "File path cannot be empty."}

    file_path = os.path.expanduser(file_path.strip())

    if not os.path.exists(file_path):
        return {"success": False, "file_path": file_path, "content": None, "size_bytes": None, "line_count": None, "message": f"File '{file_path}' does not exist."}

    if os.path.isdir(file_path):
        return {"success": False, "file_path": file_path, "content": None, "size_bytes": None, "line_count": None, "message": f"'{file_path}' is a directory, not a file."}

    size_bytes = os.path.getsize(file_path)

    try:
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()
        line_count = content.count("\n") + (1 if content and not content.endswith("\n") else 0)
        return {
            "success": True,
            "file_path": file_path,
            "content": content,
            "size_bytes": size_bytes,
            "line_count": line_count,
            "message": f"Read {size_bytes} bytes ({line_count} lines) from '{file_path}'."
        }
    except UnicodeDecodeError:
        return {"success": False, "file_path": file_path, "content": None, "size_bytes": size_bytes, "line_count": None, "message": f"Cannot decode '{file_path}' as {encoding}. Try a different encoding."}
    except PermissionError:
        return {"success": False, "file_path": file_path, "content": None, "size_bytes": size_bytes, "line_count": None, "message": f"Permission denied: cannot read '{file_path}'."}
    except Exception as e:
        return {"success": False, "file_path": file_path, "content": None, "size_bytes": None, "line_count": None, "message": f"Unexpected error: {e}"}