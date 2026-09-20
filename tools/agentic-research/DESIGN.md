# Principles for (agentic) research: design note

A single self-contained page (`index.html`), no dependencies, no network, answers and read
marks in `localStorage` (`agr_v1`). Built from the "Principles for (agentic) research" talk
deck and its source post, pitched at principles rather than tools.

## What changed from the deck

- **Reorganized.** The deck ran intro-to-agents, principles for research, principles for
  agents. The page runs: (1) why do research at all, (2) taste and how it is trained, (3) what
  an agent is, (4) running agents as a supervisor, (5) your audit. The reader meets the
  question before the tools, the discriminator before the practices that use it, and every
  agent practice is attached to the research principle it applies (context is "most problems
  are communication problems" for a new collaborator; the emulated group is "never work alone";
  loop and reiterate is the postmortem).
- **Key points only.** 38 principles, each as a statement, the reasoning in a few sentences,
  and a practice. Transitions, personal remarks, career details, anecdotes about named people
  and most quotes are left out; one quote stays where the quote is the principle.
- **The deck's drawings are on the page.** The talk's figures are inline SVG in the deck; the
  page reuses them as they are, in navy panels that keep the slide look, at full card width so
  the labels read. Drawings that were built over several slides (the access-and-permissions
  ladder, the earned-or-borrowed speed routes, the jagged frontier, the activation barrier,
  the three guardrails, the emulated group, the loop) keep their steps behind a small stepper
  with a caption per step. The six terms (container, connector, skill, harness, rule, hook) sit next
  to their definitions in the ladder explorer, four with the deck's icons and two drawn for the page.
- **Key points, not prose.** A statement, the figure, two to five bullets in the deck's own
  words (slide text and speaker notes, without the personal remarks and without invented
  one-liners), an "in practice" line, and an example: the talk's own shown in full, an
  invented illustration folded behind a toggle and labeled as invented. An earlier version
  carried a 200-word explanation per card and read as a wall of text; the bullets replaced
  it. Code examples fold under their titles. Each section opens with a short
  introduction.
- **Examples are complete.** The feedback on the talk asked for concrete examples and for
  what hooks, tests and rules actually look like. The page shows ten copyable artifacts in
  full: a CLAUDE.md for a research repository, a hook configuration and the script it runs, a
  permissions rules block, a test file (hand-computed case, differential test, a
  double-count guard), a skill file with a "when this was wrong before" section, a
  sub-agent prompt that emulates a research group with the disagreement rule in it, a Makefile
  for "script what you can", a postmortem template, and the delegation sum with worked numbers.
  The examples are written for the page in the shape of the real files, not copied from any
  repository.
- **Reviewed twice.** An audience check (a first-year with a chatbot only, a fourth-year who
  runs terminal agents daily, a phone skimmer) and a devil's advocate (factual and technical
  claims checked against the Claude Code docs, missing counter-cases, debatable sorter
  verdicts, the tools' thresholds) fed a fix pass. A second round checked every finding
  against the rendered page and caught what the first pass broke (a sentence pasted twice,
  three-versus-four counts, a skill asserting a rule the rules block did not have); the
  copyable blocks parse as strict JSON, Python, Make and bash. A later pass (devil's advocate,
  audience check, and a voice audit against the author's register) found the artifacts
  contradicting one another (a skill calling results read-only while its Makefile rewrote
  them; a CLAUDE.md ordering the agent into a denied write; a command that does not exist in
  the author's own tool) and the page's own frontier claim contradicting its jagged-frontier
  card; those are fixed, and the sorter, keep/drop test and audit now say where a verdict is a
  judgment call.
- **Interactive where a question or a calculation earns it.** A prompt per section with a
  saved answer; a ladder explorer for the six rungs (access, what it may do, who checks, what
  goes wrong first) with the six terms defined; a keep/drop test for generative skills; a
  delegation calculator (ask + wait + check over the success rate, with the "I cannot check
  it" case handled as the caveat rather than a number); a jagged-frontier sorter (ten tasks
  of similar apparent difficulty, mark what you would delegate, reveal the sort by
  checkability with reasons; five of the ten are marked arguable and show amber whichever way
  the reader sorted them, because their verdict is conditional on a check the reason names); a
  five-question audit for one task with a copyable result (an unanswerable check still vetoes,
  and the veto says why the other answers do not change it); read marks per principle with a
  progress bar. The keep/drop test grades by how many of its four reasons hold: two or more
  keeps, one keeps with a revisit, none lets go. None of the tools scores ordinary diligence
  as a mistake; where a verdict is a judgment call the reveal says so.
- **Two diagrams** redrawn as inline SVG: generator and discriminator, and the three loop
  arrangements (open loop, agent as coach, judge by the dozen).

## Voice

Peer address, sentence case, American English, typographic quotes, no emoji, no first person.
The caveat ("if you don't know, how do you check?") opens and closes the agent section, as the
talk plan asked.

## Prose gate

`tools/.limpid/check.sh agentic-research` lifts the reader-facing prose out of `index.html` and
runs the limpid CLI over it; `tools/.limpid/trace.py` maps a finding back to the line that
produced it. See `tools/.limpid/README.md`.
