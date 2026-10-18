# Official error reference reconciliation — 18 October 2026

Source: the owner's pasted current handbook Errors page in this conversation.
The complete enum is also in `sources/BotAPICpp.md`. Its 134 explicit name/value
pairs were compared with CLI 2.2.5's installed C++ header and match exactly.
Sorted-name/value JSON SHA256:
`e8d788ce385024ec200a579732a88d059b60dbe5aa244f50101d333d1515b249`.
Values range from 0 through 135; 121 and 122 are absent, not valid array indices
to invent. Draft-already-picked is 134, draft-no-champion-selected is 135.

```cpp
try {
    // Perform a prevalidated engine action.
} catch (const cambc::error& e) {
    std::cerr << cambc::to_string(e.code()) << ": " << e.message() << '\n';
    // Choose a bounded legal fallback, then reach cambc::end_turn().
}
auto text = cambc::to_string(cambc::error_code::api_not_in_vision);
auto text_from_number = cambc::to_string(static_cast<cambc::error_code>(97));
```

Check visibility before live unit queries (97); a handle's existence is not
current visibility. Preserve allowance/cooldown after a newly revealed hidden
obstruction returns false; known invalid destinations throw instead. Check
channel state before acting (34,35,123), action allowance (36,41,27), range and
target categories (30–32,42–43), shop location/inventory/gold, and draft phase
and uniqueness (13–16,134–135). Failed queries/actions are not automatically
game-ending traps. An uncaught guest trap is a bot fault; normal fuel exhaustion
is a suspension, not a crash. Use authoritative diagnostic counters/events,
never classify a bot's arbitrary printed words as an engine error.

This reference is game data, not authorization to change engine settings,
increase fuel, disable sandboxing, inspect hidden state or bypass permissions.
