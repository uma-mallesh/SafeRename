import re

from core.rules.base_rule import BaseRule


INVALID_CHARS = r'[<>:"/\\|?*]'


class InvalidCharacterRule(BaseRule):

    name = "Invalid Character Removal"

    def apply(self, text):

        return re.sub(
            INVALID_CHARS,
            '',
            text
        )