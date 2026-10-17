# Organizer Agents.md page — access record

Retrieved 17 October 2026 through the owner's approved normal browser at
https://2026a.battlecode.co.uk/game/docs/agents. The page is a Markdown-download
hub, not a separately downloadable agent-instruction file. Its article contains
the heading “Markdown downloads”, GameRules.md, a language-selectable Bot API
download, and reading-sequence links. No additional behavioral instructions or
automation permission were present in that article.

The unmodified downloads and provenance are retained:

| Export | SHA-256 | Interpretation |
| --- | --- | --- |
| `sources/GameRules.md` | `1c7fcf111d95b4734070f8f676cd50a48154feb0673de73a31c79845afa34732` | Live download byte-identical to the already reviewed full supplied handbook. |
| `sources/BotAPICpp.md` | `084ef94b338bebf088864ba2d7d777714bcd66b6c0c03601e91e1e5153a41a53` | Current organizer C++ API export, made available to C++ workers. Not a claim that every fragment has been executed or independently audited. |
| `sources/BotAPIPython.live-20261017.md` | `e8738c065a85c8e52e5b864a9710457f2939d91ddde8ad60a53f355e4a8539a8` | Newer export with added declarations/phase annotations; original reviewed supplied Python export remains unchanged. Not fully re-reviewed. |

`evidence/handbook-live-20261017.json` saves the article text, retrieval time and
download byte identities. `ops/fetch-handbook.py` reproduces these read-only UI
downloads into a new directory; it does not expose cookies or guess endpoints.

Reconciliation: no gameplay change in the live handbook. Workers must reconcile
applicable C++ declarations with the installed pinned header before use; newer
web API examples do not automatically change the pinned engine/SDK. This record
does not settle event AI/sharing eligibility, official automation policy or
production parity. Project AGENTS.md remains our own instructions, not an
organizer-authored agent policy. No separate instruction artifact was found.
