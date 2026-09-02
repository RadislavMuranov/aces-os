# P1 Provider Evidence Register

**Evidence classes used in this pack:** VERIFIED-BY-OFFICIAL-SPEC · PARTIAL · PROVIDER-VERIFICATION-REQUIRED · DEFERRED  
**Not used:** VERIFIED-BY-LIVE-SYSTEM (no live access this gate)

---

## Obsidian

| Claim area | Source | Tier | Class |
|------------|--------|------|-------|
| Vault = folder + subfolders | https://docs.obsidian.md/Plugins/Vault | Official developer docs | VERIFIED-BY-OFFICIAL-SPEC |
| Path-based file access in API examples | same | Official | VERIFIED-BY-OFFICIAL-SPEC |
| delete() vs trash() | same | Official | VERIFIED-BY-OFFICIAL-SPEC |
| Vault rename renames folder | https://obsidian.md/help/manage-vaults | Official help | VERIFIED-BY-OFFICIAL-SPEC |
| Obsidian Sync multi-device races | — | — | PROVIDER-VERIFICATION-REQUIRED |
| Plugin metadata completeness | — | — | PROVIDER-VERIFICATION-REQUIRED |

## GitHub

| Claim area | Source | Tier | Class |
|------------|--------|------|-------|
| Git ref = mutable pointer to commit SHA | https://docs.github.com/rest/git/refs | Official | VERIFIED-BY-OFFICIAL-SPEC |
| Branch is a ref; can be rewritten | same | Official | VERIFIED-BY-OFFICIAL-SPEC |
| REST resources use owner/repo path params | https://docs.github.com/rest/overview/resources-in-the-rest-api | Official | VERIFIED-BY-OFFICIAL-SPEC |
| Issue/PR numeric `id` / `node_id` in API models | GitHub REST reference (issues/PRs) | Official | VERIFIED-BY-OFFICIAL-SPEC |
| Force-push / ref update implications for tip content | refs + git model | Official + derived constraint | PARTIAL |

## Slack

| Claim area | Source | Tier | Class |
|------------|--------|------|-------|
| Message `ts` unique per channel | https://docs.slack.dev/reference/events/message | Official | VERIFIED-BY-OFFICIAL-SPEC |
| Update/delete keyed by channel + ts | https://docs.slack.dev/messaging/modifying-messages ; chat.update / chat.delete | Official | VERIFIED-BY-OFFICIAL-SPEC |
| message_deleted / edited subtypes; original text not always available after edit | message event docs | Official | VERIFIED-BY-OFFICIAL-SPEC |
| event_id on Events API envelope | Events API examples | Official | VERIFIED-BY-OFFICIAL-SPEC |
| Retention / Enterprise Grid completeness | — | — | PROVIDER-VERIFICATION-REQUIRED |

## Gmail

| Claim area | Source | Tier | Class |
|------------|--------|------|-------|
| Message `id` immutable; separate `threadId` | https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages | Official | VERIFIED-BY-OFFICIAL-SPEC |
| Thread resource distinct | users.threads resource | Official | VERIFIED-BY-OFFICIAL-SPEC |
| internalDate ordering semantics | Message resource fields | Official | VERIFIED-BY-OFFICIAL-SPEC |
| history.list startHistoryId; non-contiguous; validity window | https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.history/list | Official | VERIFIED-BY-OFFICIAL-SPEC |
| RFC Message-ID header ≠ Gmail API message id | Official API fields vs RFC headers (secondary note) | Official + documented distinction | VERIFIED-BY-OFFICIAL-SPEC |

## Google Drive

| Claim area | Source | Tier | Class |
|------------|--------|------|-------|
| File `id` is resource id; path is not identity | https://developers.google.com/workspace/drive/api/reference/rest/v3/files | Official | VERIFIED-BY-OFFICIAL-SPEC |
| trashed flag; trash vs permanent delete | File resource + delete/trash methods | Official | VERIFIED-BY-OFFICIAL-SPEC |
| Revisions list/get; revisionId; keepForever | https://developers.google.com/workspace/drive/api/guides/manage-revisions | Official | VERIFIED-BY-OFFICIAL-SPEC |
| Shortcut mime + targetId | File shortcutDetails | Official | VERIFIED-BY-OFFICIAL-SPEC |
| Shared-drive permission edge cases | — | — | PROVIDER-VERIFICATION-REQUIRED |

## Kaiten

| Claim area | Source | Tier | Class |
|------------|--------|------|-------|
| Spaces/boards/cards with integer `id` (+ space `uid`) | https://developers.kaiten.ru (space list/board/card responses via developers.kaiten.ru & extracted docs) | Official API | VERIFIED-BY-OFFICIAL-SPEC |
| Card condition enum live/archived/deleted; state queued/inProgress/done | Card response attributes in API docs | Official | VERIFIED-BY-OFFICIAL-SPEC |
| Webhooks card:add/update, comment, board, file, space | Community/extracted API docs citing developers.kaiten.ru | Official-derived | PARTIAL |
| Rate limit ~5 rps | Extracted API general info | Official-derived | PARTIAL |
| Full event payload / id stability under all moves | — | — | PROVIDER-VERIFICATION-REQUIRED |
| Delete constraints (e.g. time logs) | Secondary SDK docs | Tier 4 | PROVIDER-VERIFICATION-REQUIRED |
