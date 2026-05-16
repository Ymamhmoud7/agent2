import os
import fnmatch


def search_files(
    root_dir: str,
    pattern: str = "*",
    search_content: str = None,
    max_results: int = 100,
    recursive: bool = True
) -> dict:
    """
    Search for files by name pattern and optionally by content.

    Args:
        root_dir:       Directory to search in (e.g. "~/documents").
        pattern:        Glob-style filename pattern (e.g. "*.py", "report*", "*"). Defaults to "*".
        search_content: If provided, only return files whose content contains this string.
                        Binary files are skipped during content search.
        max_results:    Maximum number of matching file paths to return. Defaults to 100.
        recursive:      If True, search subdirectories recursively. Defaults to True.

    Returns:
        dict with keys: success (bool), root_dir (str), matches (list[str]),
                        match_count (int), truncated (bool), message (str)
    """
    if not root_dir or not root_dir.strip():
        return {"success": False, "root_dir": root_dir, "matches": [], "match_count": 0, "truncated": False, "message": "Root directory cannot be empty."}

    root_dir = os.path.expanduser(root_dir.strip())

    if not os.path.exists(root_dir):
        return {"success": False, "root_dir": root_dir, "matches": [], "match_count": 0, "truncated": False, "message": f"Directory '{root_dir}' does not exist."}

    if not os.path.isdir(root_dir):
        return {"success": False, "root_dir": root_dir, "matches": [], "match_count": 0, "truncated": False, "message": f"'{root_dir}' is a file, not a directory."}

    matches = []
    truncated = False

    try:
        if recursive:
            walker = os.walk(root_dir)
        else:
            entries = os.listdir(root_dir)
            walker = [(root_dir, [], entries)]

        for dirpath, dirnames, filenames in walker:
            # Skip hidden directories
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]

            for filename in filenames:
                if not fnmatch.fnmatch(filename, pattern):
                    continue

                full_path = os.path.join(dirpath, filename)

                if search_content is not None:
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            if search_content not in f.read():
                                continue
                    except (UnicodeDecodeError, PermissionError, OSError):
                        continue

                matches.append(full_path)

                if len(matches) >= max_results:
                    truncated = True
                    break

            if truncated:
                break

        match_count = len(matches)
        trunc_note = f" (results capped at {max_results})" if truncated else ""
        content_note = f" containing '{search_content}'" if search_content else ""
        return {
            "success": True,
            "root_dir": root_dir,
            "matches": matches,
            "match_count": match_count,
            "truncated": truncated,
            "message": f"Found {match_count} file(s) matching '{pattern}'{content_note} in '{root_dir}'{trunc_note}."
        }

    except PermissionError:
        return {"success": False, "root_dir": root_dir, "matches": matches, "match_count": len(matches), "truncated": False, "message": f"Permission denied while searching '{root_dir}'."}
    except Exception as e:
        return {"success": False, "root_dir": root_dir, "matches": matches, "match_count": len(matches), "truncated": False, "message": f"Unexpected error: {e}"}