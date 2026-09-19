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
   one discriminating feature) and *Spot the flaw* (a plan, four diagnoses, one right; reveal
   includes the repair — recognition vs repair). Before the reveal the player states confidence
   (coin flip 50% / leaning 70% / sure 90%). Scoring: right & sure +3, right & leaning +2, right &
   coin +1; wrong & sure −3, wrong & leaning −1, wrong & coin 0. The result screen reports
   accuracy, taste points, average stated confidence, a **calibration** verdict (three-bin
   ECE-lite, explained with the weather-forecaster analogy), the discriminating features missed,
   the player's own "why" notes, and a cumulative **discriminator level** (Untrained → Calibrating
   → Sharp → Reviewer they ask for).
3. **Field guide** — the full pitfall catalogue by phase with hit/dodged counts from this device,
   and every linked resource in one list.

## Content

- 39 pitfalls, 47 scenario cards, 15 pairwise items, 16 spot-the-flaw items, 62 resources.
- Resources are Path to PhD posts (developing taste, idea triage, hypotheses need to be
  predictive, multiple working hypotheses, strong inference, method vs problem orientation,
  contingency plans, quit-and-grit, open-loop postmortems, single measure/complex thing, …) plus
  the canonical rigour literature (Lipton & Steinhardt; Kapoor & Narayanan; Henderson et al.;
  Bouthillier et al.; Agarwal et al.; Dodge et al.; Melis et al.; Recht et al.; Geirhos et al.;
  Nagarajan & Kolter; Zhang et al.; Gelman & Loken; Simmons et al.; Kerr; Ioannidis; Button et al.;
  Nosek et al.; Hurlbert; Leek et al.; Platt; Chamberlin; Hamming; Feynman; Tao; Peyton Jones;
  Karpathy).
- All content lives in the `DOMAINS / PHASES / RESOURCES / PITFALLS / CARDS / PAIRS / FLAWS`
  constants at the top of the script; adding a card is adding an object.

## Deep links

`?domain=ml_exp|ml_theory|comp|lab|social|any` and `?mode=run|taste|guide`.

## Accessibility and UX

Keyboard: A/B/C(/D) to choose, 1/2/3 for confidence, Enter for next. Visible focus rings,
`aria-pressed` chips, dark mode via `prefers-color-scheme` (with `data-theme` overrides), no
horizontal scroll at 375 px. Copy-summary buttons on both result screens.
