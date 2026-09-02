"""Read-only capabilities only. Write ops are not authorized in Phase I/II."""

from __future__ import annotations

from enum import Enum


class Capability(str, Enum):
    READ_RESOURCE = "READ_RESOURCE"
    OBSERVE_RESOURCE = "OBSERVE_RESOURCE"
    LIST_RESOURCE = "LIST_RESOURCE"
    READ_METADATA = "READ_METADATA"


# Explicitly NOT authorized in this gate:
FORBIDDEN_CAPABILITIES = frozenset(
    {
        "CREATE",
        "UPDATE",
        "DELETE",
        "EXECUTE",
        "DELEGATE",
        "AUTHORIZE",
        "REVOKE",
        "WRITE",
        "MUTATE",
    }
)

READ_ONLY_CAPABILITIES = frozenset(c.value for c in Capability)
