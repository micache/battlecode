# Capital-aware gold-only camp selection

Bottleneck: repeated gold-only farming after sufficient capital, rather than
conversion of combat work into gems. This is a source-supported causal hypothesis,
not a reconstructed turn trace.

Evidence: evaluated edit 50a0d7d5 / 6d66a77f on engine 2.2.5, evaluation ca52f534.
Ambush loss 394a1869 (A) ended 394:1014 submitted, zero own deaths or lost bags;
Ryth/Marcella earned 1137/945 gold with zero collected gems. Pilgrimage loss
0349d039 (A vs frozen gamma 1b34f42a / 3ce565f6) ended 272:1044 with zero own
deaths/lost bags; Tavi/Ryth collected zero and earned 770/700. Ambush loss
c52237a0 (B) is a contrasting mixed failure: 1148 collected but 908 submitted,
240 lost in bags. New camp policy is not expected to solve bag loss by itself.
Full match IDs in saved summary filenames/provenance and NOTES; all are offline
final statistics, never runtime inputs. Exact ambush opponent identity is not
provided by these summaries; roster resembles gamma but is not identity proof.

Chosen policy: at 300 gold of cash plus our actual equipment purchase value,
add a bounded +90 score cost to zero-gem groups in the cheap shortlist AND final
ranking. Preserve ongoing captures first. The cap equals 30 geometric travel
steps, so gold remains a fallback against extremely remote, unavailable or
blocked gem groups. Count combined emblems at five paid shards, including
Power (whose extra stat point is not extra gold); Tavi's spending cannot reset
the threshold. No new search, opponent reads or live memory protocol.

Expected: more farmers collect/submit gems on ambush and pilgrimage; higher
matched wins and submitted gems. Falsifier: no win gain, lower submitted gems,
or more deaths/faults/fuel suspension on matched development cases.

Alternatives: healthy shopping repeats a zero-gain experiment and cannot change
which groups are preferred. Full reachable value/time scheduler previously had
an interlock regression and adds fuel/query costs. Frozen gamma uses value/time
and observed respawns; we adapt the objective-value distinction while retaining
beta's bounded cheap scheduler. Frozen older beta d2d57274 / 7daa9117 has our
same capped gem bonus and no capital-dependent gold penalty. No opponent copied.

Risk: more travel/danger toward gem camps, less gold growth, or penalty too small
to break distant loops. Capture availability bonus and commitment can still
justify nearby gold. Existing geometry/cooldown uncertainty remains.
