from pathlib import Path


INVALID_WINDOWS_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4",
    "LPT1", "LPT2", "LPT3"
}


def validate_transaction(original_path, new_name):

    issues = []

    target_path = Path(original_path).parent / new_name

    # Empty filename
    if not new_name.strip():

        issues.append("Empty filename.")

    # Reserved Windows names
    if Path(new_name).stem.upper() in INVALID_WINDOWS_NAMES:

        issues.append(
            f"Reserved system filename: {new_name}"
        )

    # Filename length
    if len(new_name) > 255:

        issues.append(
            "Filename exceeds 255 characters."
        )

    # Existing target collision
    if target_path.exists():

        issues.append(
            f"Target already exists: {target_path.name}"
        )

    return issues