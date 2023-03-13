from idd_ai.plugins import test_plugin
from idd_ai.plugins.plugin import FixedPlugin, Plugin, has_fixed_contract

plugins = [test_plugin]

__all__ = ["test_plugin", "plugins", "Plugin", "FixedPlugin", "has_fixed_contract"]
