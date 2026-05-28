import re

from core.rules.base_rule import BaseRule


class WhitespaceRule(BaseRule):

    name = "Whitespace Normalization"

    def apply(self, text):

        text = text.replace(" ", "_")

        text = re.sub(r'_+', '_', text)

        return text.strip('_')