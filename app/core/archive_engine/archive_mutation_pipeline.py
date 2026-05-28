import shutil

from pathlib import Path

from core.archive_engine.archive_transaction import (
    ArchiveTransaction
)

from core.archive_engine.archive_extractor import (
    extract_archive
)

from core.archive_engine.archive_rebuilder import (
    rebuild_archive
)

from core.archive_engine.archive_validator import (
    validate_archive
)

from core.archive_engine.checksum_engine import (
    calculate_file_checksum
)

from core.sanitizer.filename_sanitizer import (
    sanitize_filename
)


def process_archive(zip_path):

    transaction = ArchiveTransaction()

    temp_dir = transaction.begin()

    try:

        # -----------------------------------
        # EXTRACT
        # -----------------------------------

        extraction_result = extract_archive(
            zip_path,
            temp_dir
        )

        if extraction_result is not True:

            return {
                "status": "failed",
                "reason": extraction_result
            }

        # -----------------------------------
        # SANITIZE EXTRACTED FILES
        # -----------------------------------

        for file_path in Path(temp_dir).rglob('*'):

            if file_path.is_file():

                safe_name = sanitize_filename(
                    file_path.name
                )

                safe_path = (
                    file_path.parent /
                    safe_name
                )

                file_path.rename(safe_path)

        # -----------------------------------
        # BUILD NEW ARCHIVE
        # -----------------------------------

        rebuilt_archive = (
            Path(zip_path).parent /
            f"{Path(zip_path).stem}_rebuilt.zip"
        )

        rebuild_result = rebuild_archive(
            temp_dir,
            rebuilt_archive
        )

        if rebuild_result is not True:

            return {
                "status": "failed",
                "reason": rebuild_result
            }

        # -----------------------------------
        # VALIDATE
        # -----------------------------------

        if not validate_archive(rebuilt_archive):

            return {
                "status": "failed",
                "reason": "Archive validation failed"
            }

        # -----------------------------------
        # CHECKSUM
        # -----------------------------------

        checksum = calculate_file_checksum(
            rebuilt_archive
        )

        return {
            "status": "success",
            "rebuilt_archive": str(
                rebuilt_archive
            ),
            "checksum": checksum
        }

    finally:

        transaction.cleanup()