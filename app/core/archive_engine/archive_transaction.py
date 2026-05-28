import tempfile
import shutil
from pathlib import Path


class ArchiveTransaction:

    def __init__(self):

        self.temp_dir = None

    def begin(self):

        self.temp_dir = Path(
            tempfile.mkdtemp(
                prefix="saferename_"
            )
        )

        return self.temp_dir

    def cleanup(self):

        if self.temp_dir and self.temp_dir.exists():

            shutil.rmtree(
                self.temp_dir,
                ignore_errors=True
            )