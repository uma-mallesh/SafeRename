from pathlib import Path
import emoji

from core.sanitizer.filename_sanitizer import sanitize_filename


def contains_emoji(text):

    return emoji.emoji_count(text) > 0


def scan_folder(folder_path):

    problematic_files = []

    for file_path in Path(folder_path).rglob("*"):

        if file_path.is_file():

            original_name = file_path.name

            cleaned_name = sanitize_filename(original_name)

            if original_name != cleaned_name:

                problematic_files.append({
                    "original": original_name,
                    "cleaned": cleaned_name,
                    "path": str(file_path)
                })

    return problematic_files