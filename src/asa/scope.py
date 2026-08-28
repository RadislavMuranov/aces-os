"""Scope evaluation: resource selector form A/B + operations (I3).

Prohibited: glob, regex, CEL, pattern languages.
"""

from __future__ import annotations

from .types import (
    Capability,
    Operation,
    ResourceKind,
    ResourceRef,
    ResourceSelectorExact,
    ResourceSelectorStructured,
)


def resource_in_scope(resource: ResourceRef, capability: Capability) -> bool:
    selector = capability.resource_selector
    if isinstance(selector, ResourceSelectorExact):
        if not selector.resource_ids:
            return False
        return resource.resource_id in selector.resource_ids
    if isinstance(selector, ResourceSelectorStructured):
        if not selector.kinds:
            return False
        if resource.resource_kind not in selector.kinds:
            return False
        if selector.namespace is not None:
            if resource.namespace != selector.namespace:
                return False
        return True
    return False


def operation_in_scope(operation: Operation, capability: Capability) -> bool:
    if not capability.operations:
        return False
    return operation in capability.operations


def scope_allows(resource: ResourceRef, operation: Operation, capability: Capability) -> bool:
    return resource_in_scope(resource, capability) and operation_in_scope(operation, capability)
