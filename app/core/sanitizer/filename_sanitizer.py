import re
import emoji

from pathlib import Path

from core.intelligence.extension_rules import (
    get_file_category
)

from core.intelligence.media_patterns import (
    preserve_media_patterns
)


INVALID_CHARS = r'[<>:"/\\|?*]'


def remove_emojis(text):

    return emoji.replace_emoji(
        text,
        replace=''
    )


def normalize_spaces(text):

    text = text.replace(" ", "_")

    text = re.sub(r'_+', '_', text)

    return text.strip('_')


def sanitize_filename(filename):

    path = Path(filename)

    stem = path.stem

    extension = path.suffix

    category = get_file_category(extension)

    preserved_patterns = []

    # ----------------------------------------
    # MEDIA-AWARE PROCESSING
    # ----------------------------------------

    if category == "media":

        preserved_patterns = preserve_media_patterns(
            stem
        )

    # ----------------------------------------
    # REMOVE EMOJIS
    # ----------------------------------------

    cleaned = remove_emojis(stem)

    # ----------------------------------------
    # REMOVE INVALID CHARS
    # ----------------------------------------

    cleaned = re.sub(
        INVALID_CHARS,
        '',
        cleaned
    )

    # ----------------------------------------
    # NORMALIZE SPACES
    # ----------------------------------------

    cleaned = normalize_spaces(cleaned)

    # ----------------------------------------
    # RESTORE PRESERVED PATTERNS
    # ----------------------------------------

    for pattern in preserved_patterns:

        if pattern not in cleaned:

            cleaned += f"_{pattern}"

    # ----------------------------------------
    # FALLBACK
    # ----------------------------------------

    if not cleaned:

        cleaned = "renamed_file"

    return f"{cleaned}{extension}"