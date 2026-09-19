# Research Pitfalls — The Study Game (design note)

A lightweight, text-only, self-contained game for junior PhD students setting up a study.
Served at `/tools/research-pitfalls/` (a static file without front matter, copied verbatim by
Jekyll, like `tools/research-values/`). One `index.html`, inline CSS/JS, no build step, no CDN,
no backend; progress in `localStorage`.

## Audience and focus

First-year PhD student about to design a study. Machine learning (experimental and theory) is
the main focus; a domain selector re-voices the same pitfalls for computational/simulation
science, experimental/lab science, and social & behavioral science, and adds a few that are
native to each (pseudoreplication, batch effects, blinding, measurement validity,
convergence studies). "General" shows only the domain-neutral cards.

## Four parts

1. **Run a study** — 13 decisions across five phases (Question → Design → Execution → Analysis →
   Reporting). Each card is a situation with 2–3 options tagged `sound`, `pit` (names a pitfall
   from the catalog) or `meh` (defensible but costly). Two meters: weeks spent (budget 22; an
   all-sound run uses at most 21; going over demotes the verdict one band) and rigor, which
   starts at 100 and is scored *relative to the deck*: each card can lose at most (best option −
   worst option) rigor points, so the final number is 100 × (1 − losses / total possible losses)
   and does not depend on card order. Verdict bands: Ready for review (≥ 82) · Fixable: major
   revision (≥ 58) · Redesign (≥ 35) · Back to the question. A phase stepper shows one colored
   dot per decision; every choice gets a verdict with an icon and a text badge; pitfalls get a
   *what / smells like / instead* tile row plus a collapsed **worked example and why it happens**
   with its reading. Ends in a **postmortem**: verdict, a rigor trajectory chart, a collapsed
   phase-by-phase map of all pitfalls marked hit/dodged, the pitfalls hit as collapsible entries,
   the defensible-but-costly calls, and a reading list. Only `sound` choices are credited as
   dodging a card's pitfalls.
   Deck: per phase, half the slots (rounded randomly for odd picks) go to domain-specific cards
   and the rest to universal ones, then shuffled. The Analysis phase has no universal card left
   after the theory split, so it draws only from the domain's own pool.
2. **Train your taste** — gamifies the discriminative skill from *P2P No. 135 — Developing taste*
   (taste is trainable by judging many examples with dense feedback and articulating why). The
   player picks one of two **tracks** per round, because they are different skills and most
   students struggle with the first:
   - *Taste for developing ideas* (default): pairs of full **idea pitches** for the same kind
     of work that differ in one feature (a measurement that can say no, a mechanism with a
     prediction, a confound named and separated, rule out before you prove, relax the
     assumption that fails); **grow a weak idea** (a weak pitch and four next moves, one of
     which turns it into a question); **triage** (five ideas, one month, pick the first; the
     reveal shows the author's full ranking with reasons); and the short idea pairs.
   - *Taste for writing and evaluating*: pairs of **abstracts** for the same study (claims sized
     to evidence, source of the gain identified, failure cases in the abstract, comparable
     baselines, assumptions and regime stated, the bound instantiated); *Spot the flaw* (a
     plan, four same-phase diagnoses, one right; the reveal includes the repair and a collapsed
     box showing what the pitfall looks like); and the short paper pairs.

   The long-form pitches and abstracts are written for machine learning (experimental and
   theory); other domains get the short items only, and the track picker says so. Pools per
   ML domain are about 35 to 40 items per track (20 idea pairs, 12 grow items, 7 triage
   batches, 12 abstract pairs, 12 preference items, plus the short pairs and flaws), and a
   round draws **unseen items first**, then the least recently seen, so replaying a track
   samples new items until the pool is used up; the results screen says how many of the
   pool have been seen and how many are left in the other track. Every pair
   is like-for-like (two empirical ideas or two theory ideas, never one of each) and the reveal
   names the feature and a stated **principle**. Sides are shown in random order and the
   explanation's A/B letters (and the grow items' move numbers) are relabelled to match.
   After picking and *before* the reveal the player can write a one-line "why" (that is what
   trains the judge) and states confidence: guess (50% for pairs, 25% for four-option items,
   20% for triage) / leaning (70% / 60% / 50%) / sure (90% / 90% / 85%). Scoring is a roughly
   proper rule so the point-maximising choice is the honest one: right: sure +4, leaning +3,
   guess +1; wrong: sure −6, leaning −2, guess +1 (leaning beats guess above 60% belief, sure
   beats leaning above 80%, the midpoints between the stated probabilities).

   Fairness rule for every pair: both sides are the same kind of work, at the same altitude
   (a goal against a goal, a plan against a plan), in the same stated setting, and neither is
   a strawman, so only the named feature differs. A devil's-advocate pass over all 48 pairs
   rewrote eight that broke it. Extending a theorem to a known setting is valid work without
   a prediction; the theory boundary pair therefore turns on assumptions checked against the
   setting versus assumptions added until the proof goes through.

   Two **preference items** per round have no right answer: both sides are sound and the pick
   is a reading on one spectrum (no points, no confidence step). Abstract pairs ask which
   abstract makes the sounder claim, never which paper is better, since only the abstract is
   shown; abstracts do not cite figures. When a preference item comes round again and the pick
   flips, the reveal says so: a mind that moves is the point. The result screen reports
   accuracy, points, average stated confidence, a **calibration** verdict with a reliability
   diagram (per-confidence-bin accuracy against stated probability; the weighted gap is an
   expected calibration error), the discriminating features missed, the player's own notes, a
   cumulative **discriminator level** (Untrained → Calibrating → Sharp → The reviewer authors
   ask for; level points count only the first exposure to an item, so repetition does not level
   you up), and a **taste profile**: six spectra (generalist–specialist, performance–mechanism,
   builder–pilot-first, headline–rigor, method-led–question-led, provable-first–phenomenon-first),
   each with a virtue and a vice per pole, fed by the preference picks and by the graded items
   (where the game's answer sits at the right-hand pole, so a miss records the instinct that
   pulled the pick left). Hollow mark: this round; filled mark: all rounds on the device. The
   profile is descriptive, not graded, and says so.
3. **Field guide** — the full pitfall catalog by phase as expandable tiles (what / smells like /
   instead / read, plus the worked example), hit/dodged marks from this device, the player's
   taste-gym notes, a glossary of every term the game uses, and every linked resource. The
   glossary and the reading list open as collapsed groups with counts (nine glossary groups:
   statistics, design, evaluation, models, theory, code and compute, simulation, lab and social
   science, writing; seven reading groups by what the reading helps with), because the flat
   lists of about 180 terms and 73 readings were too dense to scan. The glossary search opens
   only the groups with a match and hides the rest.

## Didactic design (after a learning-science review)

- **Contrast at the moment of feedback.** After a pitfall or costly pick, the reveal shows the
  sound option and its reasoning next to the chosen one, so the learner compares rather than
  just reads a verdict. "Defensible, costly" is defined in one fixed line every time it appears.
- **Generation before feedback.** *Commit first* (a home-screen toggle, and on automatically for
  the first three decisions of a first run) hides the options until the player has written what
  they would do; the line is echoed next to the verdict. In the taste gym the "why" box comes
  before the confidence chips and gets focus on hover-capable devices; Enter or 1/2/3 from an
  empty box moves on, so the keyboard path is not interrupted.
- **Spaced review.** *Review what you fell in (N)* on the home screen builds a deck from the cards
  whose pitfalls the player has hit on this device.
- **Easy wins first.** Within a phase, cards with fewer pitfall options and fewer words come first.
- **The postmortem teaches.** "One thing to do tomorrow" prints the fix for the costliest pitfall
  hit; "Copy as checklist" emits a tick-list of fixes; "Copy for your supervisor" prepends
  "Pitfalls I want to avoid in my study". The reading list shows one item per pitfall first, the
  rest collapsed. The map marks pitfalls that are not in the chosen domain's deck as such.
- **Honest scoring copy.** A wrong guess shows "+1 · a guess is never penalized" with a one-time
  note that guessing is the honest choice below 60% belief; the calibration label is decided by
  the same per-bin error the reliability diagram shows, explained without classifier jargon.
- **Nuance lines** on absolute-sounding lessons (test set, three seeds, toy models, one message
  per paper, data that cannot be shared, pre-planned pilots) to avoid installing wrong rules.
- **Length balance.** About half the sound options now carry a short rationale and half the
  pitfall options carry none, so terseness is not a tell (sound option longest on 16 of 59
  cards, shortest on 30).

## UX (after a browser-driven review)

Why-box before confidence; term strip below the verdict so it does not compete with the
options; hover tooltips not clipped by the next option; on touch devices the underlines are
dropped (the chips carry the definitions) and keyboard hints are hidden; phase line in sentence
case with the phase blurb only on the first card of a phase; mobile stepper shows only the
current phase label; chart type sizes legible at phone width; dark-mode digits use the on-accent
token; field guide has jump links and a glossary filter; "Your taste, measured" instead of
"Your discriminator"; the top level is "The reviewer you'd want".

4. **Scope an idea** — five questions a supervisor, a reviewer and a funder all ask, each with an
   anchored 0–3 scale: novelty (ten named kinds with examples: new method, new question,
   connecting fields, new evidence, new measurement/dataset, new explanation, simplification,
   new application, new capability, new lens), impact (six kinds: changes practice, changes
   belief, enables others, settles a debate, opens a direction, beyond academia), feasibility,
   killability, fit. A live radar and a novelty-versus-feasibility map (Alon's quadrants:
   moonshot / PhD-shaped / exploit / avoid) read the shape, with a verdict and reading. Five
   sample ideas across domains carry three scorers (author, two reviewers) with rationales; the
   reveal overlays their shapes on yours and shows a per-dimension dot plot with the spread, to
   make the subjective element visible and to argue that naming the kind of novelty is what lets
   people disagree about the same thing. For your own idea, a scope statement (weeks, one claim,
   who it matters to, kill test by week N) is generated for copying. Each dimension has a
   collapsed "why this is partly subjective" note.

## Visual elements

Fourteen template pictograms (target, story, scope, clock, loop, check, fork, noise, shortcut,
leak, weights, confound, cluster, bound, select) drawn as inline SVG with theme tokens; every
pitfall maps to one, shown in the pitfall box with a caption, in the guide tiles, in the
postmortem entries and next to "one thing to do tomorrow". Phase icons replace numbers in the
stepper and guide. The home screen opens with a path-with-pits illustration. The taste reveal
tips a balance scale toward the stronger side. Charts: rigor trajectory, reliability diagram,
idea-shape radar, novelty × feasibility map, scorer dot plot.

## Voice (after an audit against the author's newsletter)

The copy addresses the player as a peer ("you"), with no first person, American spelling, sentence-case headings,
typographic quotes, names in running prose as "Lipton and Steinhardt" (ampersands only in
citations), three-author papers named in full, no emoji, jokes at the system's expense and never
the player's. Feedback strings are kept under about 35 words and worked examples under about
110. "P2P" is expanded once in the field guide.

## Terms and tooltips

Every technical term in a situation, option, plan, pair or reveal gets a dotted underline and a
hover tooltip with a one-line definition, and each card lists its terms in a tap-safe strip
underneath (the options are buttons, so a tap on an underlined word would otherwise pick the
answer). The index is built from `GLOSSARY` (`[term, definition, surface forms]`, ~180 entries
after an exhaustive audit of every decision and option text) plus the 45 pitfall names, whose
tooltip is the catalog's one-line *what*. Only the first occurrence of a term in a text block is
marked; surface forms are chosen to avoid ordinary English words (so "wells" is marked, "well" is
not). Idioms that a non-native reader might miss were reworded in the cards.

## Content

- 45 pitfalls (each with a worked example and a longer explanation), 59 scenario cards, 15
  pairwise items, 20 spot-the-flaw items (options use the catalog's pitfall names), 60
  glossary entries (about 180 with the tooltip audit), 70 resources. The "why" notes from the taste
  gym are listed in the field guide.
- Reviewed with an audience-persona pass (five first-year personas across domains) and a
  devil's-advocate pass (factual claims about cited papers verified, game logic simulated,
  scoring fairness, accessibility); both rounds' findings are folded in. Option texts are
  length-balanced so the sound answer is not the longest one; pitfall options carry a plausible
  justification.
- Resources are Path to PhD posts (developing taste, idea triage, hypotheses need to be
  predictive, multiple working hypotheses, strong inference, method vs problem orientation,
  contingency plans, quit-and-grit, open-loop postmortems, single measure/complex thing, …) plus
  the canonical rigor literature (Lipton & Steinhardt; Kapoor & Narayanan; Henderson et al.;
  Bouthillier et al.; Agarwal et al.; Dodge et al.; Melis et al.; Recht et al.; Geirhos et al.;
  Nagarajan & Kolter; Zhang et al.; Gelman & Loken; Simmons et al.; Kerr; Ioannidis; Button et al.;
  Nosek et al.; Hurlbert; Leek et al.; Platt; Chamberlin; Hamming; Feynman; Tao; Peyton Jones;
  Karpathy).
- All content lives in the `DOMAINS / PHASES / RESOURCES / PITFALLS / CARDS / PAIRS / FLAWS /
  GLOSSARY / LESSONS` constants at the top of the script; adding a card is adding an object.

## Deep links

`?domain=ml_exp|ml_theory|comp|lab|social|any`, `?mode=run|taste|scope|guide`, and `?mode=taste&track=ideas|papers`.

## Accessibility and UX

Keyboard: A/B/C(/D) to choose, 1/2/3 for confidence, Enter for next (native activation is left
alone for focused buttons, links and summaries). Focus moves to the new card's title and, after
answering, to the Next button; the verdict is a polite live region; revealed options carry text badges, not color alone;
contrast tokens (`--on-accent`, `--btn`) keep button and badge text at AA in both themes;
`prefers-reduced-motion` honoured; dark mode via `prefers-color-scheme` (with `data-theme`
overrides); no horizontal scroll at 375 px. Copy-summary buttons on both result screens.
