import threading


class PluginTimeout:

    def __init__(self, timeout=3):

        self.timeout = timeout

    def run(self, target):

        thread = threading.Thread(
            target=target
        )

        thread.start()

        thread.join(self.timeout)

        return not thread.is_alive()