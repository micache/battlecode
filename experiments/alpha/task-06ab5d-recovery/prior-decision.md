# Tribute interruption experiment

Identity: task-2087eef984f3476a8285ea2a9ffd739c / alpha. Edit base
1f5e71f3111c5a492a20f4aaf0bbd3bd0c6fff97, source dd7c6c996f40dd12888dd3e3d6e877bdf574fbd3bb16a19060260f2c33931599.
All nine files match edit commit. HEAD d5b01ab9 is the evaluated Prism trial,
not this edit source. No pending alpha candidate or interrupted edit to recover.

Hypothesis: prioritizing legal in-range stuns against visible enemy tribute
channels increases matched wins over the edit base. Nonpositive win gain falsifies
it. Enemy tribute, own tribute, deaths and interrupt usage diagnose the mechanism.
This is a rules/source deduction; supplied finals do not prove missed interrupts.

Evidence: evaluation 3d7c788a measures d5b01ab9 / 30b88729, with development
base delta -0.0054054 across 185 side pairs, zero faults/missing/unknown. Development
map contrasts include 00ambush A 1/5, B 3/5 versus 00pilgrimage and 00stampede
5/5 on each side. Those results do not evaluate the code now edited.
Manifest a12adf54 was hash-verified, including every source file of all six entries.
Boss ea15ef0f / f4b4f65e banks at 30 gems or within eight altar tiles and fights
according to local advantage; it has no stun immunity in its first three picks
Vendetta/Varg/Ryth. Our ordinary scorer caps damage at target HP, adds only 20 for
control, and starts with a basic; it has no channel-value priority. GameRules.md
273 explicitly distinguishes damage from stuns for tribute cancellation.

Alternatives rejected: capture priority/deference/follow-through already tested
(task-e3b7eed5 and older); broad retreat/routing and offensive/support/shopping
variants also have prior evidence. No new premise justified repeating them.
Free wards are untried but expose the unchanged enemy-first policy to more fights.

Plan (one coupled change, current C++ SDK):
1. Compile-time eligibility tests: active positive-bag tribute qualifies; ordinary
   combat, zero bags and stun immunity do not. Record initial failed trusted build.
2. Add bounded pre-basic denial helper in tribute_denial.h; inspect two ready
   slots, at most six fresh visible enemies, select largest interruptible bag.
   Legal tools: positive-duration unit/ground stun, enhanced reset plus legal basic.
   Refresh target state/range before action. No chasing, dash, shared bytes or RNG.
3. Integrate only at start of champion fight; keep channels/recovery and camp
   combat unchanged. End fight after success so movement cannot follow a cast.
4. Run final bot-check and inspect exact diagnostics and both smoke summaries;
   update compact NOTES with actual results. No publication or comparative games.

Risks: opportunity may be rare; interrupted enemies can restart next turn; an
interrupt can be worse than lethal damage or banking. Low-fuel fallback retains
the base fight. The guard is a planning reserve until runtime checks measure it.
