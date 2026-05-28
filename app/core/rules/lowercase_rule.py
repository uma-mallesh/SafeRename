from core.rules.base_rule import BaseRule


class LowercaseRule(BaseRule):

    name = "Lowercase Conversion"

    def apply(self, text):

        return text.lower()