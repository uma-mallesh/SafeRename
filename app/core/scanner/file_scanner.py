from pathlib import Path
import emoji


def contains_emoji(text):
    return emoji.emoji_count(text) > 0


def scan_folder(folder_path):

    files_with_emoji = []

    for file_path in Path(folder_path).rglob("*"):

        if file_path.is_file():

            filename = file_path.name

            if contains_emoji(filename):

                files_with_emoji.append({
                    "name": filename,
                    "path": str(file_path)
                })

    return files_with_emoji