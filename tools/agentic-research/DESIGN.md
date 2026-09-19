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
  with a caption per step. The four term icons (container, connector, skill, harness) sit next
  to their definitions in the ladder explorer.
- **Every principle is open and explained.** A statement, the figure, a 120-to-220-word
  explanation carrying the argument a listener would have heard (claim, why, counter-case,
  what changes in practice), a concrete example (the deck's where it has one, marked as new
  otherwise), and an "in practice" line. Long explanations are split at a sentence boundary
  near the middle. Each section opens with a short introduction from the chapter notes.
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
  verdicts, the tools' thresholds) fed a fix pass; see the commit history.
- **Interactive where a question or a calculation earns it.** A prompt per section with a
  saved answer; a ladder explorer for the six rungs (access, what it may do, who checks, what
  goes wrong first) with the four terms defined; a keep/drop test for generative skills; a
  delegation calculator (ask + wait + check over the success rate, with the "I cannot check
  it" case handled as the caveat rather than a number); a jagged-frontier sorter (eight tasks
  of similar apparent difficulty, mark what you would delegate, reveal the sort by
  checkability with reasons); a five-question audit for one task with a copyable result; read
  marks per principle with a progress bar.
- **Two diagrams** redrawn as inline SVG: generator and discriminator, and the three loop
  arrangements (open loop, agent as coach, judge by the dozen).

## Voice

Peer address, sentence case, American English, typographic quotes, no emoji, no first person.
The caveat ("if you don't know, how do you check?") opens and closes the agent section, as the
talk plan asked.
