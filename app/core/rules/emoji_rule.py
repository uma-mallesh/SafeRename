import emoji

from core.rules.base_rule import BaseRule


class EmojiRule(BaseRule):

    name = "Emoji Removal"

    def apply(self, text):

        return emoji.replace_emoji(
            text,
            replace=''
        )