from uuid import uuid4


class TempNodeGenerator:

    def generate(self, original_path):

        return (
            f"{original_path}"
            f".safetemp."
            f"{uuid4().hex[:8]}"
        )