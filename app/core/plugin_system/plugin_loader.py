import importlib.util

from pathlib import Path

from core.plugin_system.plugin_registry import (
    PluginRegistry
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

            registry.register(plugin)

        except Exception as error:

            print(
                f"Plugin load failed: "
                f"{plugin_file.name}"
            )

            print(error)

    return registry