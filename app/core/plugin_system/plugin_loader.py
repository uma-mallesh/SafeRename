import importlib.util

from pathlib import Path

from core.plugin_system.plugin_registry import (
    PluginRegistry
)

from core.security.plugin_validator import (
    validate_plugin
)

from core.security.crash_guard import (
    protected_plugin_call
)

from core.security.plugin_timeout import (
    PluginTimeout
)


PLUGIN_FOLDER = Path("plugins")


registry = PluginRegistry()


def load_plugins():

    if not PLUGIN_FOLDER.exists():

        return registry

    for plugin_file in PLUGIN_FOLDER.glob("*.py"):

        try:

            module_name = plugin_file.stem

            spec = importlib.util.spec_from_file_location(
                module_name,
                plugin_file
            )

            module = importlib.util.module_from_spec(
                spec
            )

            spec.loader.exec_module(module)

            plugin = module.Plugin()

            # ---------------------------------
            # VALIDATE
            # ---------------------------------

            if not validate_plugin(plugin):

                print(
                    f"Invalid plugin: "
                    f"{plugin_file.name}"
                )

                continue

            # ---------------------------------
            # TIMEOUT PROTECTION
            # ---------------------------------

            timeout_guard = PluginTimeout()

            if not timeout_guard.run(
                lambda: plugin.get_rule()
            ):

                print(
                    f"Plugin timeout: "
                    f"{plugin.plugin_name}"
                )

                continue

            # ---------------------------------
            # CRASH GUARD
            # ---------------------------------

            result = protected_plugin_call(
                plugin
            )

            if result is None:

                continue

            registry.register(plugin)

        except Exception as error:

            print(
                f"Plugin load failed: "
                f"{plugin_file.name}"
            )

            print(error)

    return registry