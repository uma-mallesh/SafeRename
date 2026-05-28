class VirtualFilesystem:

    def __init__(self):

        self.files = []

    def add_file(self, virtual_file):

        self.files.append(virtual_file)

    def all_files(self):

        return self.files