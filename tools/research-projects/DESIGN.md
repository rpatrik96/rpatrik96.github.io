# Research Projects — *The Management Game*: design note

A single self-contained HTML page (`index.html`), no dependencies, no network, state in
`localStorage` (`rpm_v1`). Sister of the Research Pitfalls game and built on the same
stylesheet and engine helpers (tooltips, term chips, verdict boxes, profile spectra).

## What it is for

The year a PhD student first leads a project: a supervisor with no time, a senior collaborator
with many projects and few time pressures, a master's student the player is responsible for, and
a deadline in month eight. The soft-skill problems that follow (time pressure, authorship
fights, silent collaborators, dropped balls, late feedback, burnout) are not taught and are
expected. The game makes them consequences of decisions, so the player can see which decision
seeded which problem and what would have prevented it.

Sources: lab-culture discussions (roles only, no names: the PI, a student, a postdoc, a senior
collaborator), the crisis-management and feedback notes behind them (three components of
feedback, situation-behavior-impact, "can I give you some feedback?", start/stop/continue,
kind versus nice, ask for advice not feedback, "can this conflict deepen the relationship?"),
two collaboration postmortems (a project stalled across two fields and mismatched time horizons;
leading projects as the most junior member, where the coaches' answer was "you told them how
you work; have you asked how they work?"), and the Path to PhD posts on expectations, deadlines,
planning, contingency, open-loop projects, meetings, rest, failure, conflict and delegated speed.

## The people

The four characters have names and plain-language roles, because a junior player may not know
what a PI is or how a master's student ends up on a paper: Nadia (your supervisor, the PI),
Tomasz (a tenured professor at another institute who joined after a chance conversation), Lea
(a PhD student in your lab, a year ahead), Ben (the master's student you co-supervise). Every
card and message names them, with the role glossed on first mention.

A run opens with an intro screen ("Before month 1"): who you are (a second-year PhD student
running a project for the first time), what the project is, the deadline in month 8, and how
the game works, followed by the four people with a one-line role under each name ("your
supervisor, the PI"); the same role line sits under the month counter throughout the run, so a
junior player never has to remember who Nadia is.
Each run also gives each of them one of two personalities, shown on that intro screen
before month one: Nadia wants to be asked or trusts you to decide; Tomasz keeps opening doors
or wants the paper out; Lea says it straight or goes quiet; Ben asks early or hides being
stuck. This is the answer to a fair objection, that the "sound" move often depends on who the
people are. On a few cards the personality changes which option is sound (with a supervisor
who trusts you to decide, deciding and telling her beats reminding her; with a student who asks
early, a Friday note beats an hour of pairing; with a colleague who goes quiet, asking in
private whether the plan still makes sense to her comes before any request), on more cards it
changes the reason, and the reveal on every people-dependent card says so and says what the
other kind of person would need. A few problems are more or less likely with some people. The
screen says plainly that a game can carry only two versions of a person and that reading them
is part of the job.

## Voice

Every situation is a short scene (who, what happened, what you are looking at, what is at
stake) rather than a prompt, and every drill message reads like an email or a Slack message a
person would send: greetings, natural sentences, no meta-labels such as "one question, fifteen
seconds". The better message still carries context, a concrete ask, a date and a way to answer
briefly, in the way a considerate person writes, without announcing the technique: a good
message does not say "you can answer in a line", "a one-word answer is fine" or "one
disagreement, with the evidence"; it asks the question, states the disagreement and points at
the table. The weaker message in each pair is one a well-meaning person actually sends (polite,
a little vague, missing the date or the ask), not a caricature of apologies, so the choice
teaches something. Reveals refer to "the first message" and "the second"; the engine swaps the
ordinals when the pair is shown in the other order.

## Four parts

1. **Run a project.** Nine months, two decisions per month drawn from a pool of about three
   (the kickoff, the deadline week, the submission form and the postmortem are always drawn),
   plus the problems that fire. Six dials, 0 to 100: alignment, trust, buffer, credit, energy,
   loop; a progress bar; and a relationship bar per character. Every option is sound, the trap,
   or defensible-but-costly; the reveal names the effect on the dials, the reason, the sound
   move if missed, and the problem the option seeds.
   - **Seeds.** Options set named seeds (`auth_unspoken`, `expect_written`, `hero`, …). At
     the start of each month the game evaluates the problems due that month: each has a base
     risk and a `risk(state)` function that adds for the seeds that cause it and subtracts for
     the ones that prevent it, plus a few dial thresholds (energy below 35 raises burnout). A
     roll under the risk fires the problem as an incident card with a "why now" banner that
     names the decisions behind it; a roll above it when the risk was pushed below the base is
     logged as *prevented*, with the decision that did it. Some problems fire at low odds
     whatever the player did, because some cannot be avoided, only handled.
   - **Progress** grows with every decision by a base amount that the loop and alignment dials
     raise and an empty buffer or an empty tank halve; a few options add or remove progress
     directly. Submission at the deadline needs progress above 55 and buffer above zero.
   - **Outcome.** Submitted; paper quality (progress and loop); team health (trust, alignment,
     relationships); energy; credit. Verdict bands: Ran it well (75), Shipped at a cost (58),
     Survived it (40), Learned the hard way. The submission is worth 30 points, so a paper
     shipped over a broken team or an empty tank does not read as a success.
2. **Debrief (the analytics module).** A line chart of the six dials and progress over the
   year with the months a problem fired marked; a timeline that lists every problem that fired
   with its odds and the decisions it traces back to, every problem prevented with the decision
   that prevented it, and every trap or costly call with the problem it seeded; a management
   profile on five spectra (controller–servant leader, assumes–writes it down, keeps the
   peace–says the hard thing, hero–delegates, sprinter–pacer), this run hollow and all runs
   filled, each pole with a virtue and a vice; three things to do differently (the problems
   that fired first, then the lowest dials); a reading list; a copyable summary. A cumulative
   profile screen shows, across runs, which problems were hit, prevented and repaired.
3. **Say it better (the drills).** Fourteen pairs of messages for the hard moments: the
   collaborator who went quiet, the authorship opener, the reminder to a silent PI, feedback on
   a late section, asking for advice rather than feedback, declining a request, the weekly
   update, reporting a dead result, a meeting invite, disagreeing with the PI's framing, a cold
   email, checking the target venue, inviting a postmortem, telling the PI about burnout. The
   weaker message is written long on purpose (apologies, hedges, over-explanation), so length is
   not the tell; the better one carries context, a concrete ask, a date, and a way for the other
   person to answer in one line. Rounds of eight, unseen items first.
4. **Field manual.** Sixteen problems in three groups (alignment and communication; time and
   load; credit and trust), each with what it looks like, what causes it, how to prevent it, how
   to repair it once it has fired, and what to read; hit and prevented counts from this device;
   a glossary with hover tooltips on every card; the readings in five groups.

## Didactic choices

- **Delayed consequences with a visible trace.** The point of the game is that management
  failures are seeded months before they fire. Every incident banner and every debrief entry
  names the seeding decision, in the player's own words, so the lesson is causal rather than
  moral.
- **Prevented problems are shown.** Good management is invisible; the debrief makes it visible
  by listing what did not fire and why.
- **Repair is scored separately from prevention.** A fired problem has a sound repair, a trap,
  and a costly option, so the game teaches recovery as well as avoidance.
- **Both directions of subjectivity.** Which move is sound is one researcher's judgment; the
  home screen says so and every reveal gives its reasons. The profile is descriptive, and each
  pole has a virtue.
- **Voice.** Peer address, sentence case, American English, typographic quotes, no emoji, no
  first person outside quoted messages. Terms get a tooltip on first use per card.

## Deep links

`?mode=run|drills|manual|profile`.
