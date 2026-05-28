from pathlib import Path
import shutil


def undo_renames(rename_log):

    rollback_results = []

    # Reverse transaction order
    for operation in reversed(rename_log):

        try:

            new_path = Path(operation["new"])
            old_path = Path(operation["old"])

            # Verify renamed file exists
            if not new_path.exists():

                rollback_results.append({
                    "status": "failed",
                    "reason": f"Missing file: {new_path}"
                })

                continue

            # Prevent overwrite
            if old_path.exists():

                rollback_results.append({
                    "status": "failed",
                    "reason": f"Original path already exists: {old_path}"
                })

                continue

            # Restore original name
            shutil.move(str(new_path), str(old_path))

            rollback_results.append({
                "status": "success",
                "restored": str(old_path)
            })

        except Exception as error:

            rollback_results.append({
                "status": "failed",
                "reason": str(error)
            })

    return rollback_results