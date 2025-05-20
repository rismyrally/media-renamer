import re
import string


def sanitize_filename(name: str) -> str:
    """
    Removes characters not allowed in file or folder names.
    """

    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    return "".join(c for c in name if c in valid_chars).strip()
    # return re.sub(r'[\\\\/:*?"<>|]', "", name)


def extract_episode_number(filename: str, pattern: str) -> int | None:
    """
    Extracts the episode number from the filename assuming format like:
    'Show - 0144 - Title' or 'S01E05'
    Returns episode number as int or None
    """

    # Match patterns like 0144
    match = re.search(r"(\d{3,4})", filename)
    if match:
        return int(match.group(1))

    # Match S01E05 or s01e05
    match = re.search(r"[sS](\d+)[eE](\d+)", filename)
    if match:
        season = int(match.group(1))
        episode = int(match.group(2))
        return season * 100 + episode

    return None
