MEDIA_EXTENSIONS = {
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".webm"
}

ARCHIVE_EXTENSIONS = {
    ".zip",
    ".rar",
    ".7z"
}

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp"
}


def get_file_category(extension):

    extension = extension.lower()

    if extension in MEDIA_EXTENSIONS:
        return "media"

    if extension in ARCHIVE_EXTENSIONS:
        return "archive"

    if extension in IMAGE_EXTENSIONS:
        return "image"

    return "generic"