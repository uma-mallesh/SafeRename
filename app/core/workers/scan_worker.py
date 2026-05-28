import threading


class ScanWorker(threading.Thread):

    def __init__(self, scan_function, callback):

        super().__init__()

        self.scan_function = scan_function
        self.callback = callback

    def run(self):

        results = self.scan_function()

        self.callback(results)