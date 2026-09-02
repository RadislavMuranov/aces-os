"""Phase II read-only provider adapters (fixture-backed)."""

from .github import GitHubReadOnlyAdapter
from .gmail import GmailReadOnlyAdapter
from .drive import GoogleDriveReadOnlyAdapter
from .slack import SlackReadOnlyAdapter
from .kaiten import KaitenReadOnlyAdapter
from .obsidian import ObsidianReadOnlyAdapter

__all__ = [
    "GitHubReadOnlyAdapter",
    "GmailReadOnlyAdapter",
    "GoogleDriveReadOnlyAdapter",
    "SlackReadOnlyAdapter",
    "KaitenReadOnlyAdapter",
    "ObsidianReadOnlyAdapter",
]
