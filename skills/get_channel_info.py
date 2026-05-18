import subprocess
import json

DESCRIPTION = "Fetch metadata and recent video list for a YouTube channel URL or handle."

EXAMPLES = [
    {
        "user": "get info about the Veritasium YouTube channel",
        "plan": [{"type": "call", "function": "get_channel_info",
                  "args": {"channel_url": "https://www.youtube.com/@veritasium", "recent_videos": 5}}]
    }
]


def get_channel_info(channel_url: str, recent_videos: int = 5) -> dict:
    """
    Fetch metadata and recent uploads for a YouTube channel.

    Args:
        channel_url:   Channel URL or handle (e.g. https://www.youtube.com/@mkbhd).
        recent_videos: How many recent videos to include (default 5).

    Returns:
        dict with keys: success (bool), channel_url (str), name, subscriber_count,
                        video_count, recent_videos (list[dict]), message (str)
    """
    if not channel_url or not channel_url.strip():
        return {"success": False, "channel_url": channel_url, "message": "Channel URL cannot be empty."}

    try:
        # Fetch channel-level JSON (first entry = channel metadata in flat-playlist mode)
        cmd = [
            "yt-dlp", channel_url,
            "--dump-json", "--flat-playlist",
            "--playlist-end", str(recent_videos),
            "--quiet", "--no-warnings"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
        if result.returncode != 0:
            return {"success": False, "channel_url": channel_url, "message": result.stderr.strip() or "yt-dlp error."}

        lines = [l for l in result.stdout.strip().splitlines() if l]
        if not lines:
            return {"success": False, "channel_url": channel_url, "message": "No data returned."}

        first = json.loads(lines[0])
        channel_name = first.get("channel") or first.get("uploader") or first.get("playlist_title")
        videos = []
        for line in lines:
            data = json.loads(line)
            if data.get("_type") == "url" or data.get("id"):
                videos.append({
                    "title":    data.get("title"),
                    "url":      f"https://www.youtube.com/watch?v={data.get('id', '')}",
                    "duration": data.get("duration_string") or data.get("duration"),
                })

        return {
            "success":          True,
            "channel_url":      channel_url,
            "name":             channel_name,
            "subscriber_count": first.get("channel_follower_count"),
            "video_count":      first.get("playlist_count"),
            "recent_videos":    videos[:recent_videos],
            "message":          f"Fetched {len(videos)} recent video(s) for '{channel_name}'."
        }

    except FileNotFoundError:
        return {"success": False, "channel_url": channel_url, "message": "yt-dlp not found. Install with: pip install yt-dlp"}
    except subprocess.TimeoutExpired:
        return {"success": False, "channel_url": channel_url, "message": "Request timed out."}
    except Exception as e:
        return {"success": False, "channel_url": channel_url, "message": f"Unexpected error: {e}"}