REQUIRED_ATTRIBUTES = [

    "plugin_name",

    "plugin_version",

    "plugin_author",

    "plugin_permissions"
]


def validate_plugin(plugin):

    for attribute in REQUIRED_ATTRIBUTES:

        if not hasattr(plugin, attribute):

            return False

    return True