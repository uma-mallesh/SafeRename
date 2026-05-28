from core.plugin_system.plugin_contract import (
    PluginContract
)

from core.rules.lowercase_rule import (
    LowercaseRule
)


class Plugin(PluginContract):

    plugin_name = "Lowercase Plugin"

    def get_rule(self):

        return LowercaseRule()