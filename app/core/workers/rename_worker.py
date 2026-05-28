import threading


class RenameWorker(threading.Thread):

    def __init__(self, rename_function, callback):

        super().__init__()

        self.rename_function = rename_function
        self.callback = callback

    def run(self):

        result = self.rename_function()

        self.callback(result)