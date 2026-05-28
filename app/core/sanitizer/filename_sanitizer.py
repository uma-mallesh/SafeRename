from pathlib import Path

from core.rules.rule_pipeline import (
    RulePipeline
)

from core.rules.emoji_rule import (
    EmojiRule
)

from core.rules.invalid_char_rule import (
    InvalidCharacterRule
)

from core.rules.whitespace_rule import (
    WhitespaceRule
)

from core.rules.lowercase_rule import (
    LowercaseRule
)


DEFAULT_RULES = [

    EmojiRule(),

    InvalidCharacterRule(),

    WhitespaceRule(),

    LowercaseRule()
]


pipeline = RulePipeline(DEFAULT_RULES)


def sanitize_filename(filename):

    path = Path(filename)

    stem = path.stem

    extension = path.suffix

    cleaned = pipeline.process(stem)

    if not cleaned:

        cleaned = "renamed_file"

    return f"{cleaned}{extension}"