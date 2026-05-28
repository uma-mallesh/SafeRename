class TransactionQueue:

    def __init__(self):

        self.queue = []

    def add(self, operation):

        self.queue.append(operation)

    def clear(self):

        self.queue.clear()

    def get_all(self):

        return self.queue

    def count(self):

        return len(self.queue)