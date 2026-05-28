import re


MEDIA_PATTERNS = [
    r"\[1080p\]",
    r"\[720p\]",
    r"\[4K\]",
    r"S\d+E\d+",
    r"x264",
    r"x265",
    r"HEVC"
]


def preserve_media_patterns(filename):

    preserved = []

    for pattern in MEDIA_PATTERNS:

        matches = re.findall(
            pattern,
            filename,
            re.IGNORECASE
        )

        preserved.extend(matches)

    return preserved