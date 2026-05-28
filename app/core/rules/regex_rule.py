import re

from core.rules.base_rule import BaseRule


class RegexRule(BaseRule):

    def __init__(self, pattern, replacement):

        self.pattern = pattern

        self.replacement = replacement

    def apply(self, text):

        return re.sub(
            self.pattern,
            self.replacement,
            text
        )