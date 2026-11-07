# Three Directions: Three Good Designs, Not Three Reskins

Any new visual design first shows the user three directions as real drafts to choose from. The gate itself doesn't change: 100% triggered, no exemption for a specified style or brand, present them and stop, the choice filed into `direction-approved.md` (exemption conditions in the "narrow bridge" of SKILL.md).

This file is about **how the three directions get generated**.

## Why this way (the verdict from three problem rounds and blind tests)

**Round one problem: the three versions only swapped skins.** All three were usually one skeleton with the colors and font weights changed. The difference has to land in the layout structure, not the palette.

**Round two problem: the metaphors were trying too hard.** Forcing every version to start from a "big-idea metaphor" turned whole pages into filing cabinets, library cards, subway maps — the user's blind test lost 3 of 4.

**Round three problem: too many constraints, so it got boring.** To dodge the "AI default look", we once capped the three versions at one warm-paper serif and flagged look families like dark-plus-single-accent and hairline newspaper as yellow lights. All three versions retreated together into pale cool colors and tidy grids; the user said "too tidy, too boring", and it lost again to the old way that carried no such constraints — and among the old way's outputs, the ones the user approved were precisely dark-plus-single-accent and warm-paper serif.

So the approach now is **add options, not bans**: the three logics stay as they were, each produces two candidates, six thumbnails get drawn first, and the strongest three that are most different from one another become the full versions; styles are picked from specimens you can actually see, references are dismantled from real screenshots. Look families are no longer a defect — they only call for a change when all three versions crowd into the same family, or collide with a recently delivered project.

## The Process

### Phase 1 · Clarify the brief + ask for references up front

This is the project's one and only round of questions (no re-asking after a direction is picked; the question bank in `references/workflow.md` draws from this round), at most 3 at a time: audience / core message / emotional tone / output format. In the same round, ask for all reference material at once: what the project is called, whether there's a logo / brand colors / VI / type spec, and whether there's a site or screenshot with that "exactly this feeling" quality; if there's none of it, one sentence settles it — "your call".

If the user doesn't respond, don't sit waiting: fill in the gaps with best-judgment assumptions (marked assumption) and keep moving — replace more questions with something they can see.

A concrete brand or product name given (the kind whose logo you can find on the official site) → the Core Asset Protocol comes into play too (`references/brand-asset-protocol.md`); all three directions build on the same set of real assets, and the difference lies in interpretation. A generic subject name (coffee, history, fitness) is not a brand — don't go looking for "the logo of coffee".

### Phase 2 · Consultant-style restatement

Restate in your own words the essential need, the audience, the scenario, the emotional tone, and the expectations the user hasn't said out loud. End with "I'll go ahead and build 3 real versions in different directions for you to see" — not with "which direction do you want": a choice made before any visuals exist is invalid.

### Phase 3 · Freeze the spec

Write a thorough design spec; it is the shared input of all three directions: what the project is, audience and scenario, the core message as bullet points, emotional tone, **output format and dimensions (required, and all three versions must match — otherwise there's no comparing them side by side)**, known constraints, image needs. The spec says only "what to say", never "what it looks like" — looks are the direction card's business.

### Phase 3.5 · Materials up front

Per `references/materials.md`: decide the tier first, then fetch all the real images the content requires plus the named products' logos — shared across the three directions.

### Phase 4 · Six candidates → six thumbnails → pick three

Before writing anything, look at three things:

```bash
# $HD = this skill's root directory (the directory containing SKILL.md), not the user's project directory
python3 "$HD/scripts/learn.py" direction color <subject keywords>   # this user's preferences + lessons from past projects
python3 "$HD/scripts/design_lint.py" ledger                     # what recent deliveries looked like and which references were used: none of them again this time
```

Then open the style overviews with your vision capability: `$HD/assets/style-specimens/sheet-<section>.jpg` (sections: web / ppt / info / app / xhs Xiaohongshu, plus east, the cross-medium Chinese & East Asian section). One image holds the specimens of every style in that section — know first what each style looks like when done right.

**4a · Three logics, two candidates each (six in total):**

- **Best designer ×2**: Take a deep breath and actually think — if budget had no ceiling, which studio or designer in the world is the best fit for designing for "this user, this subject"? Come up with two of different temperaments (one bold, one restrained; or one Western, one East Asian). Adopt their design thinking and build from scratch — do not imitate the look of any single work of theirs. Don't keep landing on the same few names: beyond Pentagram, Kenya Hara, and Vignelli there are Lü Jingren, Kohei Sugiura, Ikko Tanaka, Kazunari Hattori, Irma Boom, Experimental Jetset, Collins, Studio Dumbar…
- **Real-world reference ×2**: Pick two real works in the **same medium** as the brief whose design you are certain is outstanding — for an app, find apps (Apple Design Awards); for a website, find websites (Awwwards winners, brand official sites); for a deck, find publications and proposals; for an infographic, find press graphics (SND, Malofiej winners). Same-medium references transfer the layout directly; cross-medium ones (a deck done as a Penguin cover, an app done as a herbarium specimen sheet) in real tests came out either over the top or boring. Verify it exists with WebSearch, then **screenshot it and look**:

  ```bash
  python3 "$HD/scripts/ref_board.py" <work URL or image URL> [<second one>] --out refs/board.jpg
  ```

  Open the reference board with your vision capability and write what you're borrowing as concrete rules: how many grid columns, the headline-to-body size ratio, the dominant color's share, the image-text relationship. If the screenshot fails (anti-scraping, a WebGL black screen), switch to a write-up page or image of the same work, or ask the user for a screenshot; if none of that works, write "have not seen it with my own eyes" on the card — never pretend you have.
- **Seconds roulette ×2**: Take the current seconds S (`date +%S`; on Windows PowerShell, `(Get-Date).Second`), draw number `S % style count in that section + 1` from the matching section of `references/design-styles.md`, then `S % 12 + 1` from the east section. The number is the entry's order within its section — the same numbering as the specimen filenames and the cells on the overview sheet. Open the drawn style's specimen image first (the "specimen" line in its entry) and see it done right before writing the card. If the draw lands in the same family as one of the look ledger's last 3 deliveries, move on to the next number; if fidelity is <70%, note which part was downgraded. The roulette's job is to take you somewhere you wouldn't have gone on your own.

**When the user has specified a style or brand**: all six candidates each produce one interpretation inside that context; the colors can all sit under the brand's constraints (add `--brand` to compare, which compares skeletons only); the roulette draws only from styles compatible with the context. "Apple style" is a context, not a design.

**4b · Write six direction cards** into the project directory's `directions.md`, one block each:

| Field | What to write |
|---|---|
| Logic and source | Which designer / which work (with the source and the reference-board path) / which style drawn at which number |
| What is borrowed | The concrete rules dismantled out of the source and applied to this design: grid, type relationships, color proportions, image-text relationship |
| Lead material | What the frame's protagonist is: real photos, generated images, procedural textures, data-as-image, giant type… (tiers in `references/materials.md`) |
| Skeleton | The layout structure in one sentence |
| Where the daring goes | The one boldest spot; everything else serves the content |
| Where the form grew out of the content | One sentence: which thing in this design only this subject could have |

**4c · Draw six thumbnails.** One `design-demos/thumbs.html`, six cells, each cell the candidate's most crucial single screen (the web first screen, the deck cover, the infographic's opening, the app's main screen), roughly 480×300: real fonts, real palette, real skeleton, real headline — the details can be left out. Screenshot it, then look with your vision capability. Thumbnails are cheap, and this step exists precisely to try more styles — when a thumbnail looks wrong, swap the source and redraw that cell; you don't wait for the full build to find out.

**4d · Pick three to build in full**, criteria in order:

1. **Good enough standing alone**: you could put it in front of anyone without embarrassment. What even the thumbnail can't hold up, the full version won't rescue.
2. **The three differ from one another**: different skeletons, different temperaments (bold / neutral / quiet needn't all be there, but the three can't all sit at the same temperature), not crowding into one look family.
3. **No collision with recent projects**: looks and references the look ledger says were just used don't get picked this time.
4. **Not trying too hard**: turning the whole page into a prop or a physical replica, defaulting to a universal metaphor (subway map, terminal command line, newspaper front page, dashboard), saturation and font sizes all maxed out — at most one of the three may go this way, and only when the content truly needs it. The test: **remove the device — is the information clearer or muddier?** If removing it makes it clearer, it was too much.

The three don't need one per logic: two best-designer plus one roulette is fine — pick the strongest. Keep the three not chosen; show them to the user too at presentation time.

One example (subject: the official website of an artisanal soy sauce brewery, three generations deep):

- Best designer | Kenya Hara | Borrowed: generous whitespace, the material itself as protagonist, very few words | Lead: real photos of the clay vats and the sunning yard | Skeleton: one screen, one image, one sentence, a slow vertical pace | Daring: a full-bleed close-up of salt frost as the hero | Form: the sauce suns for 180 days, so the pace slows down
- Real-world reference | the official site of an award-winning long-established Japanese food maker (screenshot attached) | Borrowed: the relation between vertical titles and horizontal captions, the ratio of two colors, thin-ruled sections | Lead: real bottle shots + a vertical title | Skeleton: vertical title on the left, three content columns on the right | Daring: only two colors | Form: the old establishment's "family recipe" presence
- Seconds roulette | drew "Media-Grade Editorial Brutalism" | Borrowed: large type-size contrast and a modular grid | Lead: an oversized 「酱」 (the character for "sauce") cut into the hero | Skeleton: modular grid, text and images interleaved | Daring: the hero's type-size contrast | Form: one character tells the whole sauce house

### Phase 5 · Build in parallel, self-check each version

Each subagent gets only the spec + its own one direction card (with the reference board or specimen image) + the shared materials — independent contexts, no referencing each other. On runtimes without subagents, build serially: before starting each version, read only the spec and your own card, and don't reference the already-built versions.

Build rules (shared by all three versions):

- The user's real content, no Lorem; all three versions carry the same content and swap only the design
- Hard readability floors: web body text ≥14px, labels ≥12px; deck body text ≥24px, labels ≥16px; 1080-wide long-form images read on phones: body text ≥36px, labels ≥28px; body text contrast ≥4.5:1; whitespace should be composition, not absent content
- Single-file HTML; in single-file deliveries, images and logos are embedded as base64
- Decks use the deck shell, 2 representative pages per direction (`references/modules/deck.md`)
- App prototypes with multiple screens: don't just line them up as a row of phones — for the display-board composition see "Display board" in `references/app-prototype.md`
- Thumbnails go in `design-demos/thumbs.html`, the three full versions in `design-demos/dir-1.html`, `dir-2.html`, `dir-3.html` (decks use subdirectories like `dir-1/`); screenshot with `npx playwright screenshot file:///… out.png --viewport-size=1440,900` (decks use 1920,1080)

After all three are built, run:

```bash
python3 "$HD/scripts/design_lint.py" check design-demos/dir-*.html       # red lights must be fixed; yellow lights are reflexive template chrome, delete them; look family is a hint only
python3 "$HD/scripts/design_lint.py" compare design-demos/dir-*.html     # two versions collided → swap in another of the alternates, or change the skeleton — not the colors
#   if the brand constrains colors and fonts, add --brand; if the app prototype lines up several phones, add --ignore-layout; for decks add --viewport 1920x1080 --min-body 24 --min-label 16
python3 "$HD/scripts/design_lint.py" ledger check design-demos/dir-*.html # collided with a recent project → swap in another of the alternates
```

Name the full versions `design-demos/dir-1.html` through `dir-3.html`, and confirm there really are 3 before moving on. A yellow light just means delete that structure — swapping in a different symbol to slip past the detector doesn't count as a fix; look families need no fixing, they only matter when the three crowd together or collide with the ledger. Without Python Playwright installed, the script skips itself and prints the install command; in that case compare the three versions by eye from screenshots, and write this into the delivery notes.

### Phase 6 · Present, then stop

Lay out the three full-version screenshots together, each with its direction-card summary (logic and source, what is borrowed, lead material) and its one line on where the form grew out of the content; attach the thumbnail overview with one line: "the other three are alternates — if one of them catches your eye, I'll build it out in full". Present them and end the turn to wait for the user's choice, including in unattended sessions.

### Phase 7 · After the user picks

- Write "which versions were shown, the screenshot paths, the user's verbatim words" into `direction-approved.md`
- When the user's words contain a clear statement of taste ("this has zero AI feel", "too plain", "make it more like a magazine"), record them verbatim with `learn.py add --kind preference`, and spell out the scope they apply to
- Mixed picks ("A's layout + C's colors") get built as asked — note which two fields he mixed; that's more useful than remembering which color he chose. "Over the top" and "too plain" said about a version also get recorded verbatim
- Move into execution; after delivery, `design_lint.py ledger add <final file> --project <name> --note "<source: designer/work/style>"` logs one entry in the look ledger, so next time the reference is steered away from too
