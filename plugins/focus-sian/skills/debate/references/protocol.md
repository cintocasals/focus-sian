# Focus & Sian · debate protocol

Phase-by-phase instructions for the moderator: what to write, what to send to each advisor, and the templates.
Write every file in the language of the brief. Headings in the templates are given in English: translate them into
the debate language, keeping the numbering and order.

Placeholders: `{dir}` = debate folder (absolute path) · `{lang}` = language name · `{me}` / `{other}` = Focus or
Sian · `{me_id}` / `{other_id}` = `focus` or `sian`.

---

## meta.json

Create it in phase 0 and update it after every phase. The acta builder reads it.

```json
{
  "title": "Short title of the project",
  "created": "2026-09-29 18:40",
  "lang": "ca",
  "mode": "subagents",
  "status": "in-debate",
  "phase": 0,
  "version": 1,
  "brief_summary": "One line: what is being decided.",
  "summaries": {
    "2-focus": "One line: Focus's guiding principle and first move.",
    "2-sian": "One line.",
    "3-focus": "One line: Focus's main objection to Sian.",
    "3-sian": "One line.",
    "4-focus": "One line: what Focus conceded and what it holds.",
    "4-sian": "One line.",
    "5-focus": "SIGN / SIGN WITH RESERVATIONS / DO NOT SIGN, plus one line.",
    "5-sian": "Same.",
    "5-joint": "One line: the joint thesis.",
    "6": "Approved on <date> / Changes requested: ...",
    "7": "One line: what the execution prompt asks the AI to do."
  },
  "open_disagreements": 0,
  "approval": null
}
```

`status` moves through `in-debate` → `awaiting-approval` → `approved` → `prompt-delivered`. When the user
approves, set `"approval": {"date": "YYYY-MM-DD HH:MM", "decision": "approved", "words": "<user's words>"}`.

---

## Phase 0 · Brief and context dossier (moderator)

### `00-brief.md`

```
# Brief
## 1. In the owner's words
<the user's message, verbatim, in a quote block>
## 2. Restatement
- Objective:
- Scope (what is in and what is out):
- Known constraints (money, time, people, rules):
- Decision needed from the council:
- What "done" looks like:
## 3. Documents and sources
| # | Document or source | Read? | Notes |
## 4. Disclaimer
Focus and Sian are simulations inspired by the methods of Steve Jobs and Taiichi Ohno. They are not those people
and do not speak for them.
```

### `00-context.md`

Build a fact dossier from every attached or linked document and every knowledge source in the configuration.

- Extract only facts relevant to the brief. Keep numbers exactly as written in the source.
- Give each fact its source: `(file, section or page)` or `(source name, fragment path)`.
- When a configured source is a search or RAG command, derive 3 to 8 focused queries from the brief, covering both
  lenses: customer, experience, value, positioning (Focus) and demand, process, capacity, cost, lead times,
  bottlenecks (Sian). Record the queries you ran.
- If the configuration has standing instructions, copy them first, under the heading "Standing instructions from
  the owner", so both advisors see them.
- Group facts under headings: company and people · customers and demand · offer and product · process and
  operations · money · market and competitors · constraints · history of decisions.
- End with **Gaps**: what the brief does not say and the documents do not answer.
- No opinions, no recommendations. Up to about 6,000 words. Long documents stay available by path; list those paths.

Chat update: one or two lines on what the council has to work with.

---

## Phase 1 · Questions before analysing (optional)

Instruction to each advisor (parallel):

```
PHASE 1 · QUESTIONS BEFORE ANALYSING
Debate folder: {dir}
Read {dir}/00-brief.md and {dir}/00-context.md.
Language: {lang}.
You may ask the owner up to 3 questions whose answers would change your strategy. Ask for facts, not opinions.
Do not write any file. Return, for each question: the question · why it matters for your method · what you will
assume if it is not answered.
```

If you skip this phase, write `01-questions.md` saying so and why, and set `"questions_skipped": true` in
`meta.json`.

Merge both lists: remove duplicates, keep at most five questions, and ask the user in one message (a structured
question tool if available, otherwise plain text). Write `01-questions.md`:

```
# Questions before analysing
| # | Question | Asked by | Answer from the owner (or: not answered) | Assumption if not answered |
```

---

## Phase 2 · Independent strategies (parallel, blind)

Instruction to each advisor:

```
PHASE 2 · INDEPENDENT STRATEGY
Debate folder: {dir}
Read: {dir}/00-brief.md, {dir}/00-context.md and, if it exists, {dir}/01-questions.md. Open the original documents
listed in the brief only if you need detail.
Do NOT read any file whose name starts with 02-, 03-, 04-, 05-, 06- or 07-. Your strategy must be independent.
Language: {lang}.
Apply your 12-step method and write your strategy with the Write tool to {dir}/02-strategy-{me_id}.md, following
the template below. 900 to 1,600 words.
Return to the moderator only three lines: your guiding principle · your three moves (one line) · your first
experiment or demo.

TEMPLATE
# {me} · Strategy
## 1. How I read the problem
One paragraph: the problem reframed through your method.
## 2. Facts and assumptions
| # | Statement | Fact or assumption | Source or how to verify |
## 3. Diagnosis
The three to five things that matter most.
## 4. Guiding principle
One sentence.
## 5. The three moves
For each: what · why (from your method) · how we will know it works.
## 6. What we will NOT do
At least three items, each with the reason.
## 7. Plan by phases
First two weeks · first 90 days · after. With the owner role for each step.
## 8. Indicators and success criteria
Measurable, with thresholds.
## 9. Main risks and how to watch them
## 10. The first experiment or demo
What, for whom, when, and the pass or fail threshold.
## 11. Questions I would still ask
```

Chat update after both return: the guiding principle and the three moves of each, side by side if the chat allows
a table.

---

## Phase 3 · Cross-critique (parallel)

Instruction to each advisor:

```
PHASE 3 · CRITIQUE OF {other}'S STRATEGY
Debate folder: {dir}
Read: {dir}/02-strategy-{other_id}.md (the strategy you critique), your own {dir}/02-strategy-{me_id}.md, and the
brief and context if needed.
Language: {lang}.
Write your critique with the Write tool to {dir}/03-critique-by-{me_id}.md, following the template. 600 to 1,000
words. Start with the strongest part of the other strategy, specifically and without irony. Critique ideas, never
the other advisor. Quote short fragments of its text. Back every objection with a reason from your method and, when
possible, a fact.
Return to the moderator only two lines: the best thing in the other strategy · your main objection.

TEMPLATE
# {me} · Critique of {other}'s strategy
## 1. The strongest part
## 2. What I would take from it
## 3. What does not convince me
Each point: the fragment · the objection · the reason · the evidence.
## 4. Risks it has not seen
## 5. Questions for {other}
## 6. Verdict
| Element of the other strategy | Keep / Change / Drop | Why |
```

---

## Phase 4 · Rebuttal and revised position (parallel)

Instruction to each advisor:

```
PHASE 4 · REBUTTAL AND REVISED POSITION
Debate folder: {dir}
Read: {dir}/03-critique-by-{other_id}.md (the critique of your strategy), your {dir}/02-strategy-{me_id}.md, the
other strategy {dir}/02-strategy-{other_id}.md and your own critique {dir}/03-critique-by-{me_id}.md.
Language: {lang}.
Write your rebuttal with the Write tool to {dir}/04-rebuttal-{me_id}.md, following the template. 500 to 900 words.
Concede on facts: if the critique brings a fact or argument you did not have, change your position and say what
changed. Hold your ground where your method and the evidence support you, and say why. Do not average.
Return to the moderator only two lines: what you concede · what you hold.

TEMPLATE
# {me} · Rebuttal and revised position
## 1. I accept, and I change my strategy
Each: the point · what changes.
## 2. I hold, and why
## 3. Nuances
## 4. Answers to {other}'s questions
## 5. Common ground I propose
Three to five points both methods can sign.
## 6. My revised strategy in ten lines
```

---

## Phase 5 · Joint strategy

### 5a · Draft (moderator)

Read all files from phases 2 to 4. Write `05-draft-joint.md` with the template below. Rules:

- Build only from what the advisors wrote. Do not add a strategy of your own.
- Tag each move: `[F]` from Focus, `[S]` from Sian, `[F+S]` shared or merged.
- Prefer the patterns in the section "Synthesis patterns" below when the advisors clash.
- Where they still disagree after phase 4, do not choose. Put it in section 9 with both positions, the experiment
  or demo that would settle it, who should decide and by when.
- Keep facts and assumptions separate. Section 11 lists the assumptions the strategy rests on.

```
# Joint strategy · <title> · v<n>
> Status: <draft | final> · Focus: <sign | sign with reservations | does not sign> · Sian: <idem>
## 1. Joint thesis
One paragraph.
## 2. Guiding principle
One sentence.
## 3. The moves
For each: [F] / [S] / [F+S] · what · why · owner role · how we will know.
## 4. What we will NOT do
## 5. Plan by phases, with gates
First two weeks · first 90 days · after. Each gate: the go signal and the stop signal.
## 6. Indicators
Experience and value (Focus) · flow, time and cost (Sian). With thresholds.
## 7. Risks and countermeasures
## 8. How they got here
### Where they agreed from the start
### What each conceded
Focus conceded... because... · Sian conceded... because...
### What changed between phases
| Point | Focus at the start | Sian at the start | Final | Why it changed |
## 9. Open disagreements
| Point | Focus holds | Sian holds | What would settle it | Who decides | By when |
(If there are none, say so explicitly.)
## 10. Decisions for the owner
## 11. Assumptions to verify first
| # | Assumption | Why it matters | How to verify | Before which gate |
```

### 5b · Sign-off (parallel)

Instruction to each advisor:

```
PHASE 5 · SIGN-OFF OF THE JOINT STRATEGY
Debate folder: {dir}
Read {dir}/05-draft-joint.md. Check it against what you wrote in phases 2 to 4.
Language: {lang}.
Write your sign-off with the Write tool to {dir}/05-signoff-{me_id}.md. At most 300 words:
# {me} · Sign-off
Verdict: SIGN / SIGN WITH RESERVATIONS / DO NOT SIGN
Required changes (at most three): section · change · why
Misattributions: anything the draft puts in your mouth that you did not say.
What I would tell the owner, in one sentence.
Return to the moderator only the verdict and the number of required changes.
```

### 5c · Final (moderator)

Apply each required change that the other advisor would not reject (check it against its phases 2 to 4). If a
required change contradicts the other advisor's position, do not apply it: add it to section 9. Fix every
misattribution. Update the status line with both verdicts. Save as `05-joint-strategy.md`.

Rebuild the acta, set `status` to `awaiting-approval`, and present it to the user:
- Three to six lines: the joint thesis, the moves, the open disagreements and the decisions that are theirs.
- The acta (published, opened or its location).
- The question: approve, request changes, or re-debate a point.

---

## Phase 6 · Approval (user)

Write `06-approval.md`:

```
# Approval
| Date | Decision | The owner's words | What changed |
```

- **Approve** → set `status` to `approved` and go to phase 7.
- **Request changes** → change round: send both advisors the user's words and the current joint strategy and ask
  each for at most 300 words (does it accept the change, what it would adjust, any risk it adds), in parallel, to
  `06-change-<n>-focus.md` and `06-change-<n>-sian.md`. Save the current strategy as `05-joint-strategy-v<n>.md`,
  write the new version with the change and the advisors' adjustments, bump `version`, and ask again.
- **Re-debate a point** → run phases 3 and 4 again on that point only (files `03b-critique-by-*.md`,
  `04b-rebuttal-*.md`), then 5a and 5b with new files (`05b-draft-joint.md`, `05b-signoff-*.md`), so no advisor file
  is overwritten. Save the current strategy as `05-joint-strategy-v<n>.md` and write the new final
  `05-joint-strategy.md`.

Never write the execution prompt without an explicit approval in this phase.

---

## Phase 7 · Execution prompt

1. Write `07-execution-prompt.md` following `execution-prompt.md` (same folder as this file). It is written to be
   pasted into another AI, so it must stand alone: no references to the debate files.
2. Review, in parallel. Instruction to each advisor:

```
PHASE 7 · REVIEW OF THE EXECUTION PROMPT
Debate folder: {dir}
Read {dir}/07-execution-prompt.md and {dir}/05-joint-strategy.md.
Language: {lang}.
Write {dir}/07-review-{me_id}.md, at most 250 words: up to five concrete fixes (section · change · why).
Focus checks: what not to do is explicit, every piece has an owner, the demo that decides is defined, the
experience comes first.
Sian checks: every step has a "done" criterion and a stop signal, money is spent in the right order, facts and
assumptions are separated, nothing is built before it is pulled.
Return only the number of fixes.
```

3. Integrate the fixes that do not contradict the approved strategy. Set `status` to `prompt-delivered`, rebuild the
   acta and deliver: the prompt in the chat inside a code block if it is short enough, and the file.

---

## Synthesis patterns

Use them when the advisors clash. They come from the analysis of both methods.

- **Bounded bet.** Focus defines the bet and the experience; Sian sets its exposure limit (money, time, stock) and
  the signals that stop it. The launch is an explicit bet with known exposure; everything after it is pull.
- **The what and the how.** Focus decides what is done and what is refused; Sian decides how it is done without
  waste.
- **The demo is the gemba of the product.** Focus's prototype or sample is the real place where Sian observes,
  measures and finds problems before anything is produced.
- **Learn early to redo less.** Restarts are allowed before anything irreversible is committed; after that, only
  with numbers.
- **Owner and cause.** Every piece has an owner with a name (Focus); every problem is solved by finding the cause in
  the process, not in the person (Sian).
- **Few options outside, flexibility inside.** A small, clear offer for the customer; a process that absorbs
  variety cheaply.
- **Stable or moving target.** When the market is stable, the incremental path usually wins; when it moves fast or
  does not exist yet, the leap has more to say. Say which case this is.
- **Honest disagreement.** When no argument wins, define the experiment that decides and who reads the result.

---

## acta.md fallback (no Python)

Concatenate in this order, each under a level-2 heading with the phase number and name: brief, context, questions,
strategies (Focus, then Sian), critiques, rebuttals, draft joint strategy, any re-debate files (`03b-`, `04b-`,
`05b-`), sign-offs, joint strategy, previous versions (`05-joint-strategy-v<n>.md`), approval, change rounds
(`06-change-`), execution prompt, reviews. Start with the title, the date, the mode and the disclaimer.
