import zipfile


def extract_archive(zip_path, extract_to):

    try:

        with zipfile.ZipFile(zip_path, 'r') as archive:

            archive.extractall(extract_to)

        return True

    except Exception as error:

        return str(error)