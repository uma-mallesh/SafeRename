class OperationState:

    def __init__(self):

        self.cancel_requested = False

        self.total_operations = 0

        self.completed_operations = 0

    def reset(self):

        self.cancel_requested = False

        self.total_operations = 0

        self.completed_operations = 0

    def request_cancel(self):

        self.cancel_requested = True

    def increment_completed(self):

        self.completed_operations += 1

    def progress_percentage(self):

        if self.total_operations == 0:
            return 0

        return (
            self.completed_operations /
            self.total_operations
        ) * 100