# Research Values — Would You Rather (design spec)

A lightweight, self-contained static web tool that helps researchers surface their
**research values** through forced-choice ("Would You Rather") dilemmas. Two modes:

- **Values mode** — a scored questionnaire that triangulates the player's leanings across
  9 bipolar research-value axes and renders a shareable "research-values fingerprint."
- **Icebreaker mode** — a click-through generator (two options in random order, no scoring)
  for lab retreats and social use.

Builds on the vault notes *Would You Rather — Research & Life Edition*, *Values, SOLVED*
(Schwartz / Rokeach / Ryff / Aristotle), and *The Values Wheel*.

## Principles

- **The reasoning is the point.** There are no wrong answers; a forced choice is a projective
  prompt, not a test. Results are phrased as *"your choices leaned…"*, never *"you are…"*.
- **Values are a system of tensions, not a type.** Output is a 9-spoke profile, not a
  Myers-Briggs label. Each pole is a virtue whose extreme is a vice (Aristotle's golden mean).
- **Field-neutral core, optional field flavor.** The trade-offs are universal; only the
  concrete apparatus is domain-specific. ML jargon (GPUs, labeled data, code) is stripped from
  scored cards and pushed into optional field flavor / ML-tagged icebreaker cards.
- **Lightweight + portable.** One self-contained `index.html` (inline CSS/JS, inline question
  bank, `localStorage`), no backend, no build step, no CDN deps. Drops unchanged into the
  Jekyll site, Research Agora, or a standalone repo.

## The 9 research-value axes (the scoring spine)

Each card casts a signed vote on one (occasionally two) axes. `polarity` records which option
pushes toward the axis's **first-named** (positive) pole.

| # | Axis | + pole (positive) | − pole |
|---|------|-------------------|--------|
| 1 | Curiosity vs. Real-world impact | Curiosity (understanding for its own sake) | Real-world impact (what it changes in the world) |
| 2 | Rigor vs. Novelty | Rigor (correct, reproducible, slow-and-right) | Novelty (new, surprising, first-and-wrong-able) |
| 3 | Depth vs. Breadth | Depth (world expert on a niche) | Breadth (versatile generalist) |
| 4 | Theory vs. Application | Theory (a proof / principle / why) | Application (a working artifact / how) |
| 5 | Intrinsic vs. Recognition | Intrinsic (the work is the reward) | Recognition (being known/cited/awarded) |
| 6 | Autonomy vs. Security | Autonomy (freedom over what/when/how) | Security (resources, funding, stability) |
| 7 | Output vs. Sustainability | Output (intensity, volume, run hot) | Sustainability (pace, longevity) |
| 8 | Solo vs. Collaborative | Solo (deep individual focus, clear credit) | Collaborative (collective work, shared credit) |
| 9 | Open Science vs. Competitive Advantage | Openness (share everything) | Advantage (protect priority/IP) |
| 10 | Integrity vs. Expedience | Integrity (won't cut corners) | Expedience (do what it takes to land the result) |

Axes 2 and 3 are the signature *research-taste* dimensions generic value frameworks miss;
1 and 4 are kept orthogonal (why vs. medium) so "theorist ≠ automatically curiosity-driven."

## Features (locked decisions)

- **Modes:** both ship in v1.
- **Field handling:** *neutral core + field filter.* Optional "What's your field?" selector
  (`any` / `ml` / `experimental` / `theory` / `social` / `humanities`). Universal cards
  (`domains: "all"`) always show; field-tagged cards show only for their field (or when picked).
  A few cards carry a per-field `flavor` token (e.g. resources → compute/reagents/students).
- **Quantify feature ("pin this down"):** *surgical, not blanket.* A collapsed-by-default
  disclosure attached only to the ~5–7 genuinely-noisy cards, **Values mode only**, never in
  Icebreaker. Plus one global **House Rules** key in the header. Its absence on a card is a
  quality marker that the card stands on its own.
- **"Why?" capture:** optional one-line free-text under each card, **off by default**, Values
  mode only; if filled, woven into the result and the shareable summary.
- **Skip / "both equally costly":** available on every card; a split is recorded as a *live
  tension*, not discarded.
- **Result (rich + shareable):** inline-SVG 9-spoke radar · top-3 leans + live-tensions panel ·
  generated archetype + profile narrative (~8–10 archetypes, not 2⁹ types) · Schwartz-wheel
  crosswalk ("translation, not equivalence"). Share via URL hash (answers encoded, server never
  sees it), PNG export of the radar, and copy-to-clipboard summary.
- **Persistence:** answers + seed in `localStorage` — resume, retake, diff over time.

## Scoring

For each axis `k`, over answered+scored cards loading `k`:

```
raw_k   = Σ sign_i · w_{i,k}      // sign = +1 if pick is the positive pole, else −1
max_k   = Σ w_{i,k}              // total weight available among ANSWERED cards
score_k = raw_k / max_k          // ∈ [−1, +1]; self-normalizing across unequal card counts
n_k     = # answered scored cards loading k   // coverage / confidence
```

Display tick `= (score_k + 1) · 50` (50 = balanced). Axes with `n_k < 2` render greyed
("needs more signal"). `|score_k|` near 0 ⇒ surfaced as a *live tension*. Skips contribute 0
and don't inflate `max_k`. ~40 lines of vanilla JS, recomputed live.

## Architecture

Single-file: `index.html` with inline `<style>`, inline `<script type="application/json"
id="deck">` question bank, and inline app `<script>`. Hand-rolled SVG radar (no Chart.js — a
70 KB CDN dep breaks on conference Wi-Fi). State in `localStorage`; shareable state in
`location.hash` (`#v1.a=<base64url>`). Served at `/tools/research-values/` on the Jekyll site
(static files without front-matter are copied verbatim); the same file copies into Agora
(`site/static/`) or a standalone repo root unchanged.

## The deck

> **Note:** the card list below is the *first-pass* design. The audience/UX review (six field
> personas + UX/a11y/code/voice reviewers) produced a revised deck — see
> **[Revisions after audience/UX review](#revisions-after-audienceux-review)** at the end, which
> supersedes specifics here. Net result: **30 scored cards**, two ethics cards moved to icebreaker,
> several cards de-jargoned for cross-field use, and three dishonest secondary loads removed.

### Scored pool — first pass (16 keepers, recast neutral where noted · 16 new)

Keepers are referenced by their number in the original *Would You Rather — Research & Life
Edition*; `→ recast` marks ML-neutralization. Polarity letters refer to the canonical (pre-shuffle)
option order below.

**Curiosity ⟷ Consequence (axis 1)**
- K18 — frivolous product used by a billion ⟷ invisible critical infrastructure *(A=recognition/B=consequence; dual-loads axis 5)*
- N6 — discover something true & beautiful that will never matter beyond a few specialists ⟷ build something that improves a million lives but bores you *(A=curiosity, B=consequence)*
- N8 — only ask questions you find beautiful (funding suffers) ⟷ only ask questions a committee finds useful (you find them lifeless) *(A=curiosity, B=consequence)*

**Rigor ⟷ Novelty (axis 2)**
- K7 → recast — only clean, controlled, tractable problems ⟷ only messy, real-world, uncontrolled problems *(A=rigor, B=novelty)*
- N1 — 2 years making a result you already believe airtight & reproducible ⟷ chase six risky ideas, publish the 3 that look new even if some prove wrong *(A=rigor, B=novelty)* · **pin-down**
- N2 — be the person whose results everyone trusts but who's never first ⟷ the person who opens 3 directions, 2 of whose headline claims get walked back in 5 years *(A=rigor, B=novelty)*
- N3 — reproduce a rival's result before building on it (3 months, no paper of your own) ⟷ take it on faith, ship first, risk your contribution collapsing *(A=rigor, B=novelty)* · **pin-down**

**Depth ⟷ Breadth (axis 3)**
- K23 — whole PhD on one deep niche, world expert ⟷ five broad topics, master of none *(A=depth, B=breadth)*
- N10 — undisputed world expert on one narrow problem (may become a museum piece) ⟷ fast-moving generalist (always outgunned on depth) *(A=depth, B=breadth)*
- N11 — 3 more years deeper into the niche you already lead ⟷ abandon it to start at the bottom of a hot new field *(A=depth, B=breadth)*

**Theory ⟷ Application (axis 4)**
- K22 — less time on deep fundamental research ⟷ more time on practical, marketable skills *(A=theory, B=application; dual-loads axis 1)*
- N9 → neutral — produce the deepest understanding of *why* things work, rarely make anything usable ⟷ make things that work in practice and that people depend on, without being able to explain rigorously *why* *(A=theory, B=application)*

**Intrinsic ⟷ Recognition (axis 5)**
- K13 — universally recognized but deeply dissatisfied ⟷ anonymous but profoundly fulfilled *(A=recognition, B=intrinsic)*
- K3 → recast — your field's highest honor but stuck on something you find sterile ⟷ unrenowned but on a secret, world-changing project *(A=recognition, B=intrinsic; dual-loads axis 1)*
- N13 — best work in an obscure venue judged purely on merit ⟷ identical work in the most prestigious venue, where half the attention is the logo *(A=intrinsic, B=recognition)*
- N14 — mentor 10 students into thriving researchers, your ideas published under their names ⟷ pour the decade into your own output, train no one *(A=intrinsic, B=recognition; dual-loads axis 8)*

**Autonomy ⟷ Security (axis 6)**
- K21 — permanent total control over your calendar/hours ⟷ +$15k salary every year *(A=autonomy, B=security)* · **pin-down**
- K16 — tenured prof, full freedom, perpetually grant-scraping ⟷ industry scientist, huge budget, product-constrained *(A=autonomy, B=security; dual-loads axes 1,4)* · **pin-down**
- K6 → recast — doubled pay on a topic you hate ⟷ half pay on a topic you love *(A=security, B=intrinsic→ scores axis 6 A=security; dual-loads axis 5)* · **pin-down**
- K5 — skip your defense but your advisor watches every working session ⟷ a brutal 3-hour defense, then total freedom *(A=security/oversight, B=autonomy)*
- K12 — skip teaching/admin but a 1-hour commute ⟷ live next to campus but a heavy teaching/service load *(A=autonomy/protected-time, B=security/service)*
- N16 → neutral+flavor — every resource you could want, but someone else sets the agenda ⟷ total freedom on a shoestring *(A=security, B=autonomy)* · **pin-down** · flavor `{resources}`

**Output ⟷ Sustainability (axis 7)**
- K17 — high quantity of impactful papers every year ⟷ perfect work-life balance, always leaving at 5 *(A=output, B=sustainability)*
- K20 — all aspirations by 30, then a boring career ⟷ struggle your whole career, spectacular success at 65 *(A=output/early, B=sustainability/late; dual-loads axis 5)*
- N17 — run hot 5 years (2× papers, burnout risk) ⟷ run sustainably 30 years (½ output/yr, protect health) *(A=output, B=sustainability)*

**Solo ⟷ Collaborative (axis 8)**
- K9 — write a 100k-word thesis ⟷ give 100 lightning talks *(A=solo/deep, B=collaborative/communicative; dual-loads axis 3)*
- N18 → softened — irreplaceable sole author of a small, elegant, unmistakably-yours idea ⟷ one name among dozens on the landmark everyone cites for 20 years *(A=solo, B=collaborative)*
- N19 — best work alone in long uninterrupted silence ⟷ best work in a buzzing team (never sure which good ideas were yours) *(A=solo, B=collaborative)*

**Open Science ⟷ Competitive Advantage (axis 9)**
- K14 — known for absolute integrity ⟷ known for groundbreaking genius needing morally ambiguous choices *(A=open/integrity, B=advantage)*
- K19 — responsible for tech causing mass job displacement ⟷ your dream project banned globally on ethics *(A=advantage/consequence, B=open/integrity; heavy)*
- N21 → neutral — share methods, data, materials the moment you have a result (you might be scooped) ⟷ hold them private until your follow-ups are secured *(A=open, B=advantage)*
- N22 — publish every negative result and dead end ⟷ quietly bury dead ends, publish only wins *(A=open, B=advantage)*

### Icebreaker-only fun pool (unscored, field-flavored)

Originals 1, 2, 4, 8, 10, 11, 15, 24, 25, 26, 27, 28, 29, 30, 31. ML-tagged fun (`domains:["ml"]`):
1 (flaky API vs. 2010 hardware), 10 (elegant LaTeX vs. unreviewed AI figures), 11 (deleted repo
vs. spreadsheet-typo result). All scored cards are also usable in Icebreaker (scoring simply off).

### Cuts (from the 22 brainstormed new cards)

Dropped for redundancy: N4 (abstract "is this true / what if", overlaps N2), N5 (correct-obscure
vs. famous-wrong, double-loads rigor+recognition), N7 (decade fascinating/dull, overlaps N8),
N12 (idea-credited-to-another, overlaps K13), N15 (secure-someone-decides, overlaps K16), N20
(solo-assume-help, overlaps N18). Keeper 25 dropped as a near-duplicate of 17; keeper 24
(intelligence vs. relationships) moved to Icebreaker-only as life-values, not research-values.

## Validity framing (shipped in the UI)

A persistent line under the results header: *a reflective / projective instrument, not a
validated psychometric.* The 9 axes are a hand-designed taxonomy, not factor-analytically
derived; n per axis is small; many cards are deliberately under-specified. Results are a
structured mirror and a conversation starter — *"a snapshot of today's trade-offs; values drift,
retake in 6 months."* No diagnostic, hiring, or comparative-ranking use. A "How we score this"
expander keeps the method transparent.

## Revisions after audience/UX review

A nine-agent review (six field personas — ML, wet-lab, theory, social science, humanities, plus a
skeptical senior PI — and UX/accessibility, front-end, and voice reviewers) drove the following
changes. The shipped `index.html` reflects these; this section is authoritative where it conflicts
with the first-pass list above.

**Deck — 30 scored cards.** Keepers K3, K5, K6, K7, K9, K12, K13, K16, K17, K20, K21, K22, K23 (13)
plus new N1, N2, N3, N6, N8, N9, N10, N11, N13, N14, N16, N17, N18, N19, N21, N22, N23 (17).

**Cross-field de-jargoning** (the trade-off survives; the lab/compute apparatus is stripped so the
card lands for theory, wet-lab, social science, humanities, not just ML):
- **N9** (Theory↔Application): dropped "rarely able to explain *why* it works" — a literal description
  of empirical deep learning that pre-decided the axis for ML readers; now "deepest account of *why*"
  vs "knowledge people actually use — practice, policy, public understanding, or working tools."
- **K7** (Rigor↔Novelty): "clean/well-measured vs messy/noisy/real-world" read as ecological-validity
  (an *Application* distinction) and miscoded rigorous fieldwork as anti-rigor; now "pin down your
  claims and be confident they hold" vs "certainty is out of reach, some claims will be overturned."
- **N3 / N1 pin**: dropped "reproduce a result," the hard "3 months," and "1-in-5"/"replicate across
  re-runs" (meaningless for a theorist, an order of magnitude off for wet-lab); now "re-derive and
  verify … yourself," costs stated without false precision.
- **N21** (Open↔Advantage): "methods, data, and materials" → "everything your result rests on —
  methods, data, materials, code, sources" (empty for theory, one-click for ML, MTA-governed for
  wet-lab — now spans all).
- **N22**: dropped "negative results" (empirical-genre term) and the editorial "like almost everyone
  else does"; now "every dead end and failed approach."
- **N18** (Solo↔Collaborative): "one name among **dozens**" (a non-existent fate in math/humanities)
  → "one of **several** names."
- **K17** (Output↔Sustainability): "high quantity of impactful publications every single year"
  (STEM cadence) → "a steady, high-volume body of work — always something new in press."
- **K16** (Autonomy↔Security): industry/product-goals pole generalized to "a well-resourced
  position — big budget, staff, stability — bound to an agenda someone else sets."
- **N14**: dropped the "ten students" count and softened "under their names" to survive PI-authorship
  norms; the lost item is now recognition, not output volume.
- **K5** (Autonomy↔Security): de-PhD'd — "skip your defense / advisor watches" → stage-neutral
  "supervisor or manager … skipping all formal reviews."
- **K21**: "+$15,000" → "permanent 15% raise" (currency-/career-stage-neutral, inflation-proof).
- **F2** icebreaker tagged `domains:["ml"]` (was leaking a "10,000-line codebase" to every field) and
  rewritten so both options carry a cost.

**Scoring integrity** (the methodologist's findings — a radar is only as honest as its loadings):
- Removed **K20**'s *inverted* Intrinsic dual ("aspirations by 30" is recognition, was scored as
  +Intrinsic), **K6**'s content-free Autonomy dual (money ≠ autonomy), **K16**'s weak Theory dual
  (tenure ≠ theory), and **K9**'s stretchy Depth dual (a talk isn't "breadth").
- Moved the two **ethics** cards **K14** (integrity vs genius) and **K19** (job-displacement vs
  ethical ban) **off axis 8** to icebreaker-only — they measured ethics, not open-vs-closed science,
  and K19 was too heavy for a party deck. Added **N23** (shared resource vs in-house edge) as a clean
  third Open↔Advantage card. K9 recast so its B-side ("one of fifteen voices") is genuine collaboration.

**Result-page honesty:**
- Archetype demoted from bold headline to a flagged "Closest archetype — a loose match"; `pickArchetype`
  now scores by fraction-of-traits-matched (+ mass tiebreak) instead of array order.
- Schwartz crosswalk reframed as "a loose analogy … our interpretive overlay, **not** his instrument";
  fixed the indefensible **Rigor → Conformity** mapping (now "a conscientious, truth-seeking facet").
- "How we score this" now states each non-greyed axis rests on **at most two choices** — magnitude is
  direction, not precision; strength words softened to "leaned hard / leaned / leaned slightly."
- An axis can no longer appear as both a "lean" and a "live tension" (leans now require |score|≥0.2).
- Radar excludes low-signal (n<2) axes from the filled polygon and marks them hollow at the balanced
  ring, so "unknown" never looks like a deliberate 50/50.

**"Why?" note** is now surfaced back on the results screen ("Your notes") and included in the copied
summary (local only — the share link stays answers-only for privacy/length); the textarea label no
longer over-promises that the share link carries it.

**Accessibility / robustness:** global `:focus-visible` ring (textarea no longer suppresses its
outline); House Rules is a real `role="dialog"` with Escape-to-close and focus return; icebreaker has
keyboard support; ML fun-cards are gated to `field=ml` (no longer leak on the default "any"); a shared
result link is rendered ephemerally and never overwrites the viewer's own saved session; contrast and
mobile control-reachability bumps; card text injected via `textContent` and notes HTML-escaped.

**Field-native axes (added on author request).** Each persona wanted one research-taste tension the nine
shared axes miss. These now ship as **field-native axes** (`FIELD_AXES` in the code): when a specific
field is selected, the session appends two extra cards probing that field's own fault line, scored
separately and shown as a dedicated **"Your field's own axis"** result block — deliberately *not* on the
9-spoke radar, which stays legible. The axes:

| Field | Native axis | + pole ↔ − pole |
|-------|-------------|------------------|
| Machine learning / CS | Scale-leverage ↔ Ingenuity | bigger hammer (compute/data) ↔ clever idea on a shoestring |
| Experimental / lab | Big-instrument ↔ Bench-ingenuity | rare, expensive infrastructure ↔ frugal bench science |
| Theory / mathematics | Generality ↔ Concreteness | the most general theorem ↔ one hard case nailed completely |
| Social sciences | Confirmatory ↔ Exploratory | preregistered, locked-down ↔ free exploration of the data |
| Humanities | Interpretive boldness ↔ Cautious grounding | a daring, field-shifting reading ↔ the meticulous, definitive account |

"Any field" gets no native axis (it's the generic mode). A native session is **18 core + 2 native = 20
cards**; native cards never vote on the nine core axes, and the share link round-trips them.

**Integrity ↔ Expedience — added as the 10th core axis (author request).** The two ethics cards K14
(integrity vs morally-ambiguous genius) and K19 (cause harm vs accept an ethical ban) are now *scored*
on a dedicated **Integrity ↔ Expedience** axis, joined by a lighter everyday companion **N24** (report
results as-is vs present them in their most favorable light). This re-homes ethics where it belongs
instead of polluting the Open-Science axis, and takes the radar to **10 spokes**. Scored deck is now
**33 cards**; a General-field session is 20 cards (2 × 10 axes), a specific-field session 22 (+2 native).

**Later copy tweaks (author review):** axis 1's negative pole renamed *Consequence → Real-world impact*;
the "Any field" option renamed **General** (internal id stays `any` for share-link compatibility); the
"leaned hardest" labels dropped their misleading percentage (with ~2 cards/axis the score is direction,
not degree); a how-to-read line was added under the radar; and the results expander now links Schwartz's
model ([Wikipedia overview](https://en.wikipedia.org/wiki/Theory_of_basic_human_values) +
[Schwartz 2012 open-access primer](https://doi.org/10.9707/2307-0919.1116)).
