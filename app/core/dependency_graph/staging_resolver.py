from uuid import uuid4


class StagingResolver:

    def create_temp_name(self, path):

        return (
            f"{path}.safetemp."
            f"{uuid4().hex[:8]}"
        )