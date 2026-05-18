import subprocess
import os

DESCRIPTION = "Download audio from a YouTube video URL and save it as an MP3 file."

EXAMPLES = [
    {
        "user": "download audio from https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "plan": [{"type": "call", "function": "download_youtube_audio",
                  "args": {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "output_dir": "~/Music"}}]
    },
    {
        "user": "save the audio of this video as an mp3",
        "plan": [{"type": "call", "function": "download_youtube_audio",
                  "args": {"url": "https://youtu.be/abc123", "output_dir": "~/Downloads"}}]
    }
]


def download_youtube_audio(url: str, output_dir: str = "~/Downloads") -> dict:
    """
    Download audio from a YouTube video as MP3.

    Args:
        url:        YouTube video URL.
        output_dir: Directory to save the MP3 file (default ~/Downloads).

    Returns:
        dict with keys: success (bool), url (str), output_path (str|None), message (str)
    """
    if not url or not url.strip():
        return {"success": False, "url": url, "output_path": None, "message": "URL cannot be empty."}

    output_dir = os.path.expanduser(output_dir.strip())
    os.makedirs(output_dir, exist_ok=True)
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

    try:
        cmd = [
            "yt-dlp", url,
            "--extract-audio", "--audio-format", "mp3", "--audio-quality", "0",
            "--output", output_template,
            "--quiet", "--no-warnings", "--print", "after_move:filepath"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            return {"success": False, "url": url, "output_path": None,
                    "message": result.stderr.strip() or "yt-dlp download failed."}

        saved_path = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else None
        return {"success": True, "url": url, "output_path": saved_path,
                "message": f"Audio saved to: {saved_path}"}

    except FileNotFoundError:
        return {"success": False, "url": url, "output_path": None,
                "message": "yt-dlp not found. Install with: pip install yt-dlp"}
    except subprocess.TimeoutExpired:
        return {"success": False, "url": url, "output_path": None, "message": "Download timed out."}
    except Exception as e:
        return {"success": False, "url": url, "output_path": None, "message": f"Unexpected error: {e}"}