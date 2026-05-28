class PluginContract:

    plugin_name = "Unnamed Plugin"

    plugin_version = "1.0"

    plugin_author = "Unknown"

    plugin_permissions = []

    def get_rule(self):

        raise NotImplementedError