import re
import emoji
from pathlib import Path


INVALID_CHARS = r'[<>:"/\\|?*]'


def remove_emojis(text):

    return emoji.replace_emoji(text, replace='')


def sanitize_filename(filename):

    path = Path(filename)

    stem = path.stem
    extension = path.suffix

    # Remove emojis
    cleaned = remove_emojis(stem)

    # Remove invalid filesystem chars
    cleaned = re.sub(INVALID_CHARS, '', cleaned)

    # Replace spaces with underscores
    cleaned = cleaned.replace(" ", "_")

    # Remove repeated underscores
    cleaned = re.sub(r'_+', '_', cleaned)

    # Trim underscores
    cleaned = cleaned.strip('_')

    # Fallback name
    if not cleaned:
        cleaned = "renamed_file"

    return f"{cleaned}{extension}"