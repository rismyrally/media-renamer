import re
import string


def sanitize_filename(name: str) -> str:
    """
    Removes characters not allowed in file or folder names.
    """

    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    return "".join(c for c in name if c in valid_chars).strip()
    # return re.sub(r'[\\\\/:*?"<>|]', "", name)


def is_video_file(filename: str) -> bool:
    """
    Check if the given filename has a video file extension.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the filename ends with a recognized video extension
              ('.mkv', '.mp4', '.avi'), False otherwise.
    """
    VIDEO_EXTENSIONS = [".mkv", ".mp4", ".avi"]
    return any(filename.lower().endswith(ext) for ext in VIDEO_EXTENSIONS)


def extract_episode_number(
    full_relative_path: str, file_pattern: str | None = None
) -> int | None:
    """
    Extracts season and episode number from the full relative path using a file_pattern.
    Returns a unique key as season * 100 + episode, or None.
    """

    if file_pattern:
        match = re.search(file_pattern, full_relative_path, re.IGNORECASE)
        if match:
            try:
                season = int(match.group(1))
                episode = int(match.group(2))  # or group(3) based on pattern structure
                return season * 100 + episode
            except (IndexError, ValueError):
                return None
    return None
