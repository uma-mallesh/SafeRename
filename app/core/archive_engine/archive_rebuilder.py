import zipfile
from pathlib import Path


def rebuild_archive(source_folder, output_zip):

    try:

        with zipfile.ZipFile(
            output_zip,
            'w',
            zipfile.ZIP_DEFLATED
        ) as archive:

            for file_path in Path(
                source_folder
            ).rglob('*'):

                if file_path.is_file():

                    archive.write(
                        file_path,
                        file_path.relative_to(
                            source_folder
                        )
                    )

        return True

    except Exception as error:

        return str(error)