"""Deterministic local fixtures — not live verification."""

from __future__ import annotations

GITHUB_FIXTURES = {
    "commit": {
        "sha": "abc123def4567890abc123def4567890abc123de",
        "message": "fixture commit",
        "kind": "commit",
    },
    "branch": {
        "name": "main",
        "tip_sha": "abc123def4567890abc123def4567890abc123de",
        "kind": "branch",
        "mutable": True,
    },
    "repo": {
        "full_name": "example/repo",
        "id": "12345",
        "kind": "repository",
    },
}

GMAIL_FIXTURES = {
    "message": {
        "id": "msg_001",
        "threadId": "thread_001",
        "rfcMessageId": "<unique@mail.example>",
        "internalDate": "1690000000000",
        "kind": "message",
    },
    "thread": {
        "id": "thread_001",
        "kind": "thread",
    },
}

DRIVE_FIXTURES = {
    "file": {
        "fileId": "file_abc",
        "name": "doc.txt",
        "path": "/My Drive/doc.txt",
        "revisionId": "rev1",
        "kind": "file",
        "shared_drive": False,
    },
}

SLACK_FIXTURES = {
    "message": {
        "channel_id": "C01",
        "ts": "1690000000.000100",
        "text": "hello",
        "thread_ts": None,
        "kind": "message",
    },
    "thread": {
        "channel_id": "C01",
        "thread_ts": "1690000000.000100",
        "kind": "thread",
    },
}

KAITEN_FIXTURES = {
    "card": {
        "id": 42,
        "board_id": 7,
        "space_id": 1,
        "title": "fixture card",
        "condition": "live",
        "state": "queued",
        "kind": "card",
    },
}

OBSIDIAN_FIXTURES = {
    "note": {
        "path": "notes/fixture.md",
        "vault": "local-fixture-vault",
        "content_hash": "deadbeef",
        "kind": "file",
        "sync": False,
    },
}
