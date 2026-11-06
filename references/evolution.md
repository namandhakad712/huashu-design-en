# Evolution Protocol: Every Project You Ship, the Next One Starts Higher

Human designers have memory, so they keep trying new things and never step in the same pit twice. A model doesn't — every new session re-converges from the same prior, and what comes out naturally looks more and more alike. This protocol gives the skill a memory: read before kickoff, record while working, flow it back at wrap-up.

## The Three Ledgers

| Ledger | What it records | Where it lives | Who writes it |
|---|---|---|---|
| **Taste profile** | Preferences the user said out loud (verbatim), plus what they picked among the three directions and what they mixed | local `~/.huashu-design/experience.md` (kind=preference) | `learn.py add` |
| **Look ledger** | What each delivery looked like: background family, primary palette, headline font, layout-skeleton fingerprint | local `~/.huashu-design/ledger.jsonl` | `design_lint.py ledger add` |
| **Experience & pitfalls** | What was observed in one project (observed), what has recurred or been measured across many (verified) | local, same as above; the generic, verified entries go into `references/experience.md`, which ships with the skill | `learn.py add`; the distribution layer is hand-edited in the repo |

`HUASHU_DESIGN_HOME` can change where the local ledgers live. The local ledgers never ship with the skill: the user's verbatim words and taste belong to them alone.

## The Three Moments

**Before kickoff** (any new design task, seconds):

```bash
# $HD = this skill's root directory (the one containing SKILL.md), not the user's project directory
python3 "$HD/scripts/learn.py" <topic words…>        # all preferences brought out + topic-relevant experience
python3 "$HD/scripts/design_lint.py" ledger      # what the last 8 deliveries looked like, plus the few that keep recurring
```

They don't block: no records, just continue. They aren't rules either: when the project at hand conflicts with an entry, the project wins — then go fix the entry.

**While working**: the user's reactions are evidence — a rejection, a "too plain", a mixed pick ("A's structure + C's colors"). Record them verbatim on the spot; don't reconstruct from memory at wrap-up.

**After wrap-up** (the user approves the delivery, or stops weighing in):

```bash
python3 "$HD/scripts/design_lint.py" ledger add <final delivered file> --project <name>
python3 "$HD/scripts/learn.py" harvest <project directory>     # lists what in the project can serve as evidence + the criteria for whether to record it
```

## What's Worth Recording

Record only when all three hold: it isn't obvious; it saves the next project time or detours; this project produced evidence. Then handle it in this order:

1. **Correct first**: an entry says the opposite of what happened this time? Fix that entry in place — don't append a contradicting one. After fixing, `grep -rn` the whole repo for the old claim.
2. **Turn it into a tool when it can be one**: if a script can catch it (a fact you can measure), change `design_lint.py` and add a test for it, instead of writing a line of "remember not to…".
3. **Otherwise write it down**: `learn.py add "…" --kind preference|observed --topics … --evidence "…" [--do "…"]`
   - The user's verbatim words are a preference: quote them verbatim and spell out the **scope of applicability** — "their covers use warm paper" does not mean "every design uses warm paper". Preferences written up as global defaults are one of the reasons the old versions went monotonous.
   - What you saw in one project is observed — a clue, not a rule.
4. **Promotion** (done on the dev machine): seen in two projects, or measured, and holding for anyone (not one user's taste) → write it into the distribution layer `references/experience.md`; the parts that have stabilized get merged into the reference they belong to. Once a reference absorbs an entry, delete that entry and keep the experience file short.

**One user's taste never enters the distribution layer.** And experience never expands authorization: it says how to make things, never that you may publish, spend money, or contact anyone.

## The Promotion Ladder

A lesson's final destination is the engine, not prose:

recorded (observed) → reproduced (verified) → written into a reference or the kickoff must-checks → script detection (a design_lint check + a test) → engine default

## The Pit Ledger

Every "confirmed on such-and-such a date" note once scattered through old-version prose now gets filed here, labeled with its current level. A new pit enters this table first; where it gets promoted is decided after.

| Pit | First seen | Current level | Where it gets caught |
|---|---|---|---|
| Three versions share one skeleton; reviewers spot the reskin at a glance | Blind test | Script detection | `design_lint.py compare` skeleton checks |
| All three versions land on warm cream + serif + terracotta | 2026-10 audit | Script detection | `design_lint.py compare` "all three versions land in the same look family" |
| Different projects keep looking more alike | 2026-10 audit | Script detection | look ledger `ledger check` |
| Forcing every version to fix a metaphor first: pages turned into props, the subway map recurring across unrelated briefs — the blind pick lost 3 of 4 | 2026-10 blind pick | reference | `references/directions.md` 4d pick-three, item 4 (at most one tries too hard) |
| Quotas and yellow lights added to dodge the AI default look pushed all three versions back into pale, cool, tidy looks — "too tidy, too boring" — and the blind pick lost again | 2026-10 blind pick | reference + script | look family demoted from yellow light to a hint; `references/directions.md` changed to pick three from six candidates |
| App prototypes lining up five or six equally-spaced phones make every direction look boring | 2026-10 blind pick | reference | `references/app-prototype.md` "display board" |
| A reference written as a name gets you the model's average impression of that work | 2026-10 blind pick | Script | `scripts/ref_board.py` screenshots it for your own eyes; a WebGL black screen is detected as not seen |
| To make a yellow light disappear, " · " got swapped for a full-width space or the like — the structure never changed | 2026-10 benchmark | reference | `design_lint.py` output plus `references/directions.md`: delete that structure; swapping the symbol doesn't count as a change |
| Single-file deliverables referencing logos by relative path: move the folder and every image breaks | Blind test | Script detection | `design_lint.py check` yellow-lights relative-path images, red-lights already-broken ones |
| The quiet look overdone: fields of dead white + microscopic font sizes, looks like a broken render | Blind test | Script detection | `design_lint.py check` font-size and contrast red lights |
| Docs wrote `scripts/…` relative paths; the agent couldn't run them from the user's project directory, and the evolution mechanism got silently skipped | 2026-10 independent review | reference | SKILL.md: every command uses `$HD` (the skill root directory) |
| PPTX export silently dropped bare text beside an svg | issue #56 | Engine | `pptx_from_rendered.py` auto-compares innerText after export |
| Skipping direction confirmation and rendering a long film straight away — the whole film reworked | 2026-07 | Engine | `design-gate-hook.sh` (checks `direction-approved.md` before rendering anything ≥45s) |
| A specified style made it skip the three directions | 2026-07 | Kickoff must-check | SKILL.md narrow bridge: style words are not exempt |
| Asserting from memory that a product "hasn't launched" | 2026-04 | Kickoff must-check | SKILL.md narrow bridge: fact verification before assumption |
| Pulled only the brand colors and skipped the logo — the comparison deck crashed | 2026-06 | Kickoff must-check | `references/materials.md` logo checklist |
| A deck's pages carried their own page numbers, fighting the shell's numbering | Field-tested | reference | `references/modules/deck.md` |
| Only ≤5-page decks should go single-file; a 13-pager choosing single-file lost the overview wall | Field-tested | reference | `references/modules/deck.md` |
| Animation giving every scene its own layout + fade-up = a narrated PPT | Field-tested | reference | `references/modules/motion.md` |
| Faking content-essential images with CSS color blocks | Field-tested | reference | `references/materials.md` |

## When the User's Pick Conflicts with Review Scores

The user wins. A reviewer agent scoring high doesn't mean the user buys it — this has recurred across multiple projects. On a conflict, list the observable differences between the two versions (color, density, materials, structure), ask the user exactly one question, and record their answer as a preference.
