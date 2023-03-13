from typing import Protocol, TypeGuard

from idd_ai.contracts import Contract


class Plugin(Protocol):
    contract: Contract


class FixedPlugin(Protocol):
    contract: Contract
    fixed_contract: Contract


def has_fixed_contract(plugin: Plugin | FixedPlugin) -> TypeGuard[FixedPlugin]:
    return hasattr(plugin, "fixed_contract")
