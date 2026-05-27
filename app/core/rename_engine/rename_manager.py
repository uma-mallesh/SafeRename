from pathlib import Path
import shutil


def safe_rename(old_path, new_name):

    old_file = Path(old_path)

    parent_dir = old_file.parent

    new_file = parent_dir / new_name

    # Prevent overwrite
    if new_file.exists():

        raise FileExistsError(
            f"Collision detected:\n{new_file}"
        )

    # Perform rename
    shutil.move(str(old_file), str(new_file))

    # Verification
    if not new_file.exists():

        raise Exception(
            "Rename verification failed."
        )

    return {
        "old": str(old_file),
        "new": str(new_file)
    }