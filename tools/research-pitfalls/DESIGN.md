# Research Pitfalls — The Study Game (design note)

A lightweight, text-only, self-contained game for junior PhD students setting up a study.
Served at `/tools/research-pitfalls/` (a static file without front matter, copied verbatim by
Jekyll, like `tools/research-values/`). One `index.html`, inline CSS/JS, no build step, no CDN,
no backend; progress in `localStorage`.

## Audience and focus

First-year PhD student about to design a study. Machine learning (experimental and theory) is
the main focus; a domain selector re-voices the same pitfalls for computational/simulation
science, experimental/lab science, and social & behavioural science, and adds a few that are
native to each (pseudoreplication, batch effects, blinding, measurement validity,
convergence studies). "General" shows only the domain-neutral cards.

## Three parts

1. **Run a study** — 13 decisions across five phases (Question → Design → Execution → Analysis →
   Reporting). Each card is a situation with 2–3 options tagged `sound`, `pit` (names a pitfall
   from the catalogue) or `meh` (defensible but costly). Two meters: weeks spent (budget 26) and
   rigour (0–100, starts at 45). Every choice gets a verdict paragraph; pitfalls get a box with
   *what / smells like / instead* and reading. Ends in a **postmortem** (verdict from rigour and
   budget, pitfalls hit, defensible-but-costly choices, pitfalls dodged, reading list built from
   the mistakes).
   Deck: per phase, domain-specific cards are preferred, universal cards fill the rest, shuffled.
2. **Train your taste** — gamifies the discriminative skill from *P2P No. 135 — Developing taste*
   (taste is trainable by judging many examples with dense feedback and articulating why). Two
   drills alternate for 10 items: *Which is stronger?* (two plans/abstracts/claims that differ in
   one discriminating feature; sides are shown in random order and the explanation's A/B letters
   are relabelled to match) and *Spot the flaw* (a plan, four same-phase diagnoses, one right;
   the reveal includes the repair — recognition vs repair — and a collapsed box showing what the
   pitfall looks like). After picking and *before* the reveal the player can write a one-line
   "why" (that is what trains the judge) and states confidence: guess (50% for pairs, 25% for
   four-option items) / leaning (70% / 60%) / sure (90%). Scoring is a roughly proper rule so the
   point-maximising choice is the honest one: right: sure +3, leaning +2, guess +1; wrong: sure
   −2, leaning 0, guess +1. The result screen reports accuracy, points, average stated
   confidence, a **calibration** verdict with a reliability diagram (per-confidence-bin accuracy
   against stated probability; the weighted gap is an expected calibration error), the
   discriminating features missed, the player's own notes, and a cumulative **discriminator
   level** (Untrained → Calibrating → Sharp → The reviewer authors ask for). Level points count
   only the first exposure to an item, so repetition does not level you up.
3. **Field guide** — the full pitfall catalogue by phase as expandable tiles (what / smells like /
   instead / read, plus the worked example), hit/dodged marks from this device, a glossary of
   every term the game uses, and every linked resource in one list.

## Content

- 45 pitfalls (each with a worked example and a longer explanation), 58 scenario cards, 15
  pairwise items, 20 spot-the-flaw items, 32 glossary entries, 66 resources.
- Reviewed with an audience-persona pass (five first-year personas across domains) and a
  devil's-advocate pass (factual claims about cited papers verified, game logic simulated,
  scoring fairness, accessibility); both rounds' findings are folded in. Option texts are
  length-balanced so the sound answer is not the longest one; pitfall options carry a plausible
  justification.
- Resources are Path to PhD posts (developing taste, idea triage, hypotheses need to be
  predictive, multiple working hypotheses, strong inference, method vs problem orientation,
  contingency plans, quit-and-grit, open-loop postmortems, single measure/complex thing, …) plus
  the canonical rigour literature (Lipton & Steinhardt; Kapoor & Narayanan; Henderson et al.;
  Bouthillier et al.; Agarwal et al.; Dodge et al.; Melis et al.; Recht et al.; Geirhos et al.;
  Nagarajan & Kolter; Zhang et al.; Gelman & Loken; Simmons et al.; Kerr; Ioannidis; Button et al.;
  Nosek et al.; Hurlbert; Leek et al.; Platt; Chamberlin; Hamming; Feynman; Tao; Peyton Jones;
  Karpathy).
- All content lives in the `DOMAINS / PHASES / RESOURCES / PITFALLS / CARDS / PAIRS / FLAWS /
  GLOSSARY / LESSONS` constants at the top of the script; adding a card is adding an object.

## Deep links

`?domain=ml_exp|ml_theory|comp|lab|social|any` and `?mode=run|taste|guide`.

## Accessibility and UX

Keyboard: A/B/C(/D) to choose, 1/2/3 for confidence, Enter for next. Focus moves to the new
card and to the verdict (live region); revealed options carry text badges, not colour alone;
contrast tokens (`--on-accent`, `--btn`) keep button and badge text at AA in both themes;
`prefers-reduced-motion` honoured; dark mode via `prefers-color-scheme` (with `data-theme`
overrides); no horizontal scroll at 375 px. Copy-summary buttons on both result screens.
