import zipfile


def scan_zip_archive(zip_path):

    problematic_files = []

    try:

        with zipfile.ZipFile(zip_path, 'r') as archive:

            for member in archive.namelist():

                try:

                    member.encode('ascii')

                except UnicodeEncodeError:

                    problematic_files.append(member)

    except Exception:

        pass

    return problematic_files