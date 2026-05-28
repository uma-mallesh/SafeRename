def protected_plugin_call(plugin):

    try:

        return plugin.get_rule()

    except Exception as error:

        print(
            f"Plugin crashed: "
            f"{plugin.plugin_name}"
        )

        print(error)

        return None