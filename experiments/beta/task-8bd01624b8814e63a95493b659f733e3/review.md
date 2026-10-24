# Final review

Reviewed the patch against edit commit 863825b7, not HEAD's later harvest experiment. All changes are owned. No protected source/settings/opponents changed. Prepared removal of harvest headers is part of the verified edit base.

- Draft/yield, channel preservation, observation boundaries and action validation remain in the existing controller. New terrain field uses only static public geometry. It is never used by movement or combat authorization.
- SDK compute max_distance bounds the new search to 24 steps. Fuel gate is 65k, live scan still at most six, ranking at most 32 records with persistent cursor. Lower fuel defers or falls back geometrically. No budget override.
- Target under review is first in the bounded live list and keeps 1.25 hysteresis. Two rotating frontiers remain ahead of the local shortlist; duplicate current-target indices are removed. Capture hold still precedes any selection.
- Cold/unwritten field is guarded by travel_valid; cached field expires after eight rounds/six tiles. Stale-origin costs are advisory estimates, not certified shortest distances or unseen occupancy.
- No shared-memory writes. Existing last accepted champion stays in its protected snapshot/Git commit. No agents, commits or publication.

Remaining risks: local horizon cannot price a maze's full detour; anchor estimates may misprice large groups; periodic review may change a useful route; additional host field lookups can consume fuel. Small smoke fixtures cannot validate large-map reliability or tournament gains. Static assertions exercise policy boundaries, not an engine maze fixture.
