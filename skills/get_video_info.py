import subprocess
import json

DESCRIPTION = "Fetch metadata for a YouTube video URL: title, duration, views, likes, channel, upload date, description."

EXAMPLES = [
    {
        "user": "get info about this YouTube video https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "plan": [{"type": "call", "function": "get_video_info", "args": {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}}]
    }
]


def get_video_info(url: str) -> dict:
    """
    Fetch metadata for a YouTube video.

    Args:
        url: YouTube video URL.

    Returns:
        dict with keys: success (bool), url (str), title, channel, duration,
                        view_count, like_count, upload_date, description (truncated), message (str)
    """
    if not url or not url.strip():
        return {"success": False, "url": url, "message": "URL cannot be empty."}

    try:
        cmd = ["yt-dlp", url, "--dump-json", "--no-download", "--quiet", "--no-warnings"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return {"success": False, "url": url, "message": result.stderr.strip() or "yt-dlp error."}

        data = json.loads(result.stdout)
        desc = data.get("description") or ""
        return {
            "success":     True,
            "url":         url,
            "title":       data.get("title"),
            "channel":     data.get("channel") or data.get("uploader"),
            "duration":    data.get("duration_string") or data.get("duration"),
            "view_count":  data.get("view_count"),
            "like_count":  data.get("like_count"),
            "upload_date": data.get("upload_date"),          # YYYYMMDD
            "description": desc[:500] + ("…" if len(desc) > 500 else ""),
            "message":     f"Fetched info for: {data.get('title', url)}"
        }

    except FileNotFoundError:
        return {"success": False, "url": url, "message": "yt-dlp not found. Install with: pip install yt-dlp"}
    except subprocess.TimeoutExpired:
        return {"success": False, "url": url, "message": "Request timed out."}
    except Exception as e:
        return {"success": False, "url": url, "message": f"Unexpected error: {e}"}