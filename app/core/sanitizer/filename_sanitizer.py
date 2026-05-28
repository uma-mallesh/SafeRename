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

from core.plugin_system.plugin_loader import (
    load_plugins
)


DEFAULT_RULES = [

    EmojiRule(),

    InvalidCharacterRule(),

    WhitespaceRule()
]


# -----------------------------------------
# LOAD PLUGINS
# -----------------------------------------

registry = load_plugins()

for plugin in registry.get_plugins():

    try:

        DEFAULT_RULES.append(
            plugin.get_rule()
        )

    except Exception:

        pass


pipeline = RulePipeline(DEFAULT_RULES)


def sanitize_filename(filename):

    path = Path(filename)

    stem = path.stem

    extension = path.suffix

    cleaned = pipeline.process(stem)

    if not cleaned:

        cleaned = "renamed_file"

    return f"{cleaned}{extension}"