import zipfile


def validate_archive(zip_path):

    try:

        with zipfile.ZipFile(zip_path, 'r') as archive:

            bad_file = archive.testzip()

            if bad_file is not None:

                return False

        return True

    except Exception:

        return False