# Shipped Experience (huashu-design)

Findings reproduced across projects, or measured, that hold for any user. Before kickoff, `learn.py` brings out the entries matching the topic.

Maintenance rules live in `references/evolution.md`: hand-edited in the repo only; once a reference absorbs an entry, delete it; one user's taste never enters here.

## S1 · verified · topics: direction, color, typography

- Finding: left unconstrained, the three directions slide together toward warm cream backgrounds + high-contrast serif headlines + terracotta accents. This is the model's own default aesthetic (Anthropic's interaction palette), and Anthropic's official frontend-design skill (2026) lists it first among the clustering traits of AI-generated pages. The family itself isn't ugly; the problem is all three versions crowding into it and it recurring across projects (see S6).
- Next time: don't let all three versions crowd into the same look family; `design_lint.py compare` will report "all three versions land in the same look family", and `ledger check` will report a collision with recent projects.
- Evidence: internal self-tests from skill development plus three-direction screenshots from multiple projects (2026-10 audit, unpublished); the official text: https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md

## S2 · verified · topics: direction, layout

- Finding: three versions that only swap palette and fonts while sharing one layout skeleton — reviewers and users alike recognize the reskin at a glance. The differences have to land in how the information is organized.
- Next time: the three direction cards' skeletons must differ from one another; if `compare`'s skeleton-related result runs too high, go back to the cards and change the skeleton or the source. Mind the overcorrection — forcing a metaphor onto every version makes the pages try too hard (see S5).
- Evidence: internal blind tests from skill development and the 2026-10 audit (unpublished).

## S3 · verified · topics: readability, quiet, whitespace

- Finding: quiet, whitespace-lavish styles overdone turn into fields of dead white plus microscopic font sizes — at first glance the page looks like it never finished rendering, and it loses to an ordinary baseline version.
- Next time: font-size and contrast floors (web body text ≥14px, decks ≥24px, phone long-form images ≥36px in canvas pixels, contrast ≥4.5:1) exempt no style; `design_lint.py check` will throw a red light.
- Evidence: internal blind-test reviews from skill development (unpublished).

## S4 · verified · topics: assets, logo, single-file

- Finding: single-file HTML meant to be opened with a double-click, referencing images and logos with relative paths — move it one directory over and every image breaks.
- Next time: single-file deliverables embed base64, always; `design_lint.py check` yellow-lights relative-path images and red-lights already-broken ones.
- Evidence: in a blind test, six product buttons all broke and the review was lost outright.

## S5 · verified · topics: direction, metaphor, intensity

- Finding: to pull the three directions apart, forcing every version to first fix a "big-idea metaphor" turns whole pages into props (filing cabinet, library card, prescription slip) or dresses them in universal metaphors (subway map, terminal, newspaper front page). The three directions did pull apart, but the blind pick lost to versions without that constraint — and the same subway map appeared once in each of two unrelated briefs. A new kind of sameness.
- Next time: at most one of the three full versions may turn the whole page into a prop or dress it in a universal metaphor; the way to judge is to remove the device — is the information clearer or muddier?
- Evidence: the 2026-10 revision's before/after blind pick (the new approach won only 1 of 4 briefs) and the new approach reaching for the subway map twice within those 4 briefs (internal benchmark from skill development, unpublished).

## S6 · verified · topics: direction, constraint, boring

- Finding: constraints added to dodge the AI default look (at most one of three versions in warm-paper serif, a yellow light on look families, a tries-too-hard quota) pushed all three versions back together into pale cool colors and tidy grids; users called it "too tidy, too boring", and the blind pick again lost to the old approach without those constraints. The versions that won approval under the old approach were, of all things, dark background + single accent and warm-paper serif. Constraints can only remove options; removing options doesn't produce good design.
- Next time: add options, not bans — two candidates per logic, draw thumbnails first, then pick; read styles off the specimens, dismantle references off the screenshots. Look families are only for comparing the three versions and the ledger.
- Evidence: the second 2026-10 round of before/after blind picks (2 briefs, the revision lost both), internal benchmark from skill development, unpublished.

## S7 · observed · topics: direction, reference, medium

- Finding: directions whose real-world reference was an award winner in the same medium (an app referencing Apple Design Award-winning apps, a bookstore deck referencing Stripe Press) won approval; cross-medium references (a deck referencing 1935 Penguin paperback covers, an app referencing herbarium sheets) — one tried too hard, one was boring.
- Next time: real-world references prefer the same medium; cross-medium ones lend only color or type relationships, not layout.
- Evidence: 4 real-world-reference directions across the second and third 2026-10 blind-pick rounds; small sample, pending verification in more projects.

## S8 · verified · topics: direction, style, reference

- Finding: "add options, not bans" won the blind picks — two candidates per each of the three logics, thumbnails drawn first, then three picked; styles read off the specimens, references dismantled off the screenshots; look families stopped throwing yellow lights. On the same two briefs lost the round before, the revision got picked both times, and the user's verdict was "clearly better this time".
- Next time: when you hit "too monotonous" or "too much like AI", add candidates and references first — don't reach for bans first; a new ban must first survive a round of blind picks.
- Evidence: the third 2026-10 round of before/after blind picks (2 briefs, the revision won both), internal benchmark from skill development, unpublished.
