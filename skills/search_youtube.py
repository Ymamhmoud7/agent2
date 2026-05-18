import subprocess
import json

DESCRIPTION = "Search YouTube and return a list of matching videos with title, URL, duration, and view count."

EXAMPLES = [
    {
        "user": "search YouTube for lofi hip hop",
        "plan": [{"type": "call", "function": "search_youtube", "args": {"query": "lofi hip hop", "max_results": 5}}]
    },
    {
        "user": "find Python tutorial videos on YouTube",
        "plan": [{"type": "call", "function": "search_youtube", "args": {"query": "Python tutorial for beginners", "max_results": 3}}]
    }
]


def search_youtube(query: str, max_results: int = 5) -> dict:
    """
    Search YouTube and return a list of matching videos.

    Args:
        query:       Search query string.
        max_results: Maximum number of results to return (default 5).

    Returns:
        dict with keys: success (bool), query (str), results (list[dict]), message (str)
        Each result dict: title, url, duration, view_count, channel
    """
    if not query or not query.strip():
        return {"success": False, "query": query, "results": [], "message": "Query cannot be empty."}

    try:
        cmd = [
            "yt-dlp",
            f"ytsearch{max_results}:{query}",
            "--dump-json", "--no-download", "--flat-playlist",
            "--quiet", "--no-warnings"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return {"success": False, "query": query, "results": [], "message": result.stderr.strip() or "yt-dlp error."}

        videos = []
        for line in result.stdout.strip().splitlines():
            if not line:
                continue
            data = json.loads(line)
            videos.append({
                "title":      data.get("title", "Unknown"),
                "url":        f"https://www.youtube.com/watch?v={data.get('id', '')}",
                "duration":   data.get("duration_string") or data.get("duration"),
                "view_count": data.get("view_count"),
                "channel":    data.get("channel") or data.get("uploader"),
            })

        return {"success": True, "query": query, "results": videos, "message": f"Found {len(videos)} result(s) for '{query}'."}

    except FileNotFoundError:
        return {"success": False, "query": query, "results": [], "message": "yt-dlp not found. Install with: pip install yt-dlp"}
    except subprocess.TimeoutExpired:
        return {"success": False, "query": query, "results": [], "message": "Search timed out."}
    except Exception as e:
        return {"success": False, "query": query, "results": [], "message": f"Unexpected error: {e}"}