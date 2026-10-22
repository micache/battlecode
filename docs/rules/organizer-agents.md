# Organizer Agents.md page — access record

22 October: fresh official hub downloads replace the current C++ references.
GameRules.md SHA256 `d0ffc1267709acc546a3ad54c9861aca1ae2707f2a7196cdb804392955d13f94`;
BotAPICpp.md SHA256 `59c88e086a713cc80eb414f31b25e4ed5ff1be6dbcf311822eeab687cbb2d71a`.
Full rules and the C++ export delta were reviewed against CLI 3.0.5's installed
header (`894229e17d886358719abb70cac9ab5993263a0c05bf7df14fc48fa04a8336d3`).
Changes include Golem, Heart of Ruin, changed rewards/passives/spell coefficients,
five-hit locks, ten-turn ward recharge, and changed move_towards semantics.
Ward owner(), awake/asleep camp masks, in_vision(), and distance-field copy
overloads are available in the new header. The old Python export remains a
historical language-specific reference, not an instruction to reread it for C++.
The hub is still a Markdown download page, not a separate behavioral policy.
Previous claims below describe the earlier review, not the current rules.

18 October update: the owner supplied fresh root-directory exports. GameRules.md
still hashes to `1c7fcf111d95b4734070f8f676cd50a48154feb0673de73a31c79845afa34732`.
The current `sources/BotAPICpp.md` is an unchanged copy of the new supplied
export, SHA256 `b3f00c5caf707b284910a74083d3ecc519431216fd31409be876dc0e3a769213`;
the previous bytes remain in Git. The table below records the earlier retrieval,
not the new file's hash. Visibility annotations and ward::owner were added.
CLI 2.2.5's installed header lacks ward::owner; BOT_REFERENCE.md records this
upstream documentation/SDK gap explicitly. Do not patch an unofficial SDK to
pretend they are identical. The error enum matches all 134 supplied entries.

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
