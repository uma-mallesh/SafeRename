from core.plugin_system.plugin_contract import (
    PluginContract
)

from core.rules.lowercase_rule import (
    LowercaseRule
)


class Plugin(PluginContract):

    plugin_name = "Lowercase Plugin"

    plugin_version = "1.0"

    plugin_author = "UMA"

    plugin_permissions = [

        "modify_text"
    ]

    def get_rule(self):

        return LowercaseRule()