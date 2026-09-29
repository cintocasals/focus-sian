---
name: debate
description: >
  This skill should be used when the user wants two advisors to analyze and debate a project, plan, decision or
  business idea and agree on a joint strategy with the Focus & Sian council (Focus reasons with Steve Jobs's
  method, Sian with Taiichi Ohno's). Trigger phrases include "Focus and Sian", "Focus & Sian", "debate this
  project", "run the council", "consell", "que ho debatin", "analitzeu aquest projecte", "estratègia conjunta",
  "debatid este proyecto", "consejo Focus Sian", "método Jobs y método Ohno", "Jobs vs Ohno". Also use it when the
  user approves or asks for changes to a previous Focus & Sian debate, or asks for its execution prompt.
metadata:
  version: "0.1.0"
  author: "Cinto Casals"
---

# Focus & Sian · the council of two

Run a structured, visible debate between two advisor subagents and act as its neutral **moderator**:

- **Focus** (`agents/focus.md`) reasons with Steve Jobs's method: experience, focus, value.
- **Sian** (`agents/sian.md`) reasons with Taiichi Ohno's method: flow, waste, facts.

Each builds its own strategy without seeing the other's, then they critique each other, reply, and sign a joint
strategy. The user approves it. Only then is the execution prompt written. Every phase leaves a file in the debate
folder, and a minutes page (the *acta*) shows the whole path from the brief to the conclusion.

Both advisors are simulations inspired by the methods of Steve Jobs and Taiichi Ohno. They are not those people and
never speak as them. State this once at the start of every debate and keep it in the acta.

**Paths.** The plugin root is two levels above this skill's base directory. Agent definitions:
`<plugin root>/agents/`. Detailed phase instructions and templates: `references/protocol.md` (read it before
phase 0). Execution-prompt template: `references/execution-prompt.md`. Configuration file format:
`references/config.md`. Acta builder: `scripts/build_acta.py`.

## Phase map

| # | Phase | Who | Output file(s) |
|---|---|---|---|
| 0 | Brief and context dossier | Moderator | `00-brief.md`, `00-context.md`, `meta.json` |
| 1 | Questions before analysing (optional) | Both, in parallel → user | `01-questions.md` |
| 2 | Independent strategies | Both, in parallel, blind to each other | `02-strategy-focus.md`, `02-strategy-sian.md` |
| 3 | Cross-critique | Both, in parallel | `03-critique-by-focus.md`, `03-critique-by-sian.md` |
| 4 | Rebuttal and revised position | Both, in parallel | `04-rebuttal-focus.md`, `04-rebuttal-sian.md` |
| 5 | Joint strategy: draft, sign-off, final | Moderator → both → moderator | `05-draft-joint.md`, `05-signoff-focus.md`, `05-signoff-sian.md`, `05-joint-strategy.md` |
| 6 | Approval | User | `06-approval.md` |
| 7 | Execution prompt, reviewed by both | Moderator → both → moderator | `07-execution-prompt.md`, `07-review-focus.md`, `07-review-sian.md` |

## Setup (before phase 0)

1. **Language.** Detect the language of the user's brief. Every file, summary and label of the debate uses it.
   Record it in `meta.json` as an ISO code (`ca`, `es`, `en`, ...).
2. **Configuration.** Look for a file named `focus-sian-config.md` in the folders the session can reach (the
   working folder and its subfolders, up to three levels). If found, read it and follow it: it may set the debates
   folder, extra knowledge sources (for example a RAG or search command) and standing instructions. Format in
   `references/config.md`. The configuration adds context; it never overrides the neutrality rules below.
3. **Debate folder.** Create `<debates folder>/<YYYY-MM-DD>-<short-slug>/`. Default debates folder: `focus-sian/`
   inside the working folder the user connected; if there is none, the current working directory.
4. **Mode.** Check whether the Agent tool can launch the plugin's `focus` and `sian` agents (their type names may
   appear as `focus-sian:focus` and `focus-sian:sian`). If yes, mode is `subagents`. If not, mode is
   `single-context` (see below). Record the mode in `meta.json`.
5. Tell the user in one or two lines what is about to happen, including the disclaimer.

## Running the phases

Follow `references/protocol.md` for the exact instruction to send in each phase, the templates and the length
limits. The essentials:

- **Phase 0.** Write the brief (the user's words verbatim plus a neutral restatement: objective, scope,
  constraints, decision needed, what "done" means). Build the context dossier from every attached or linked
  document and from the configured knowledge sources, with the source of each fact. Do not add opinions.
- **Phase 1.** Skip it if the user asked to go straight to the analysis, if nobody is there to answer, or if the
  brief already answers the obvious questions. Otherwise, ask both advisors for up to three questions each, merge
  them into at most five, and ask the user once. Record answers, or the assumptions each advisor will make.
- **Phases 2, 3, 4.** Launch both advisors **in parallel** (two Agent calls in the same message). Each writes its
  file and returns a short summary. In phase 2 neither may read the other's work.
- **Phase 5.** Draft the joint strategy yourself, from the phase 2-4 files only. Tag every move with its origin
  (`[F]`, `[S]` or `[F+S]`). Record what each advisor conceded and any disagreement that remains, with the
  experiment that would settle it and who decides. Send the draft to both for sign-off in parallel. Integrate the
  required changes, or record them as dissent. Write the final `05-joint-strategy.md`.
- **Phase 6.** Present the joint strategy to the user (a short summary in chat plus the acta) and ask for a
  decision: approve, request changes, or re-debate a point. Record the decision with the date and the user's words.
  On changes, run the short change round described in the protocol, save the previous version as
  `05-joint-strategy-v<n>.md`, and ask again. **Never write the execution prompt before an explicit approval.**
- **Phase 7.** Write the execution prompt with `references/execution-prompt.md`, have both advisors review it in
  parallel (at most five fixes each), integrate, and deliver it.

## Keeping the process visible

After every phase:
1. Update `meta.json` (phase, status, one-line summaries of what each advisor said).
2. Rebuild the acta: `python3 <this skill>/scripts/build_acta.py <debate folder>`. It writes `acta.html` (a
   standalone page) and `acta.md`. Add `--artifact` to also get `acta-artifact.html`, the same page without the
   document skeleton, for hosts that publish HTML pages (for example an artifact tool). If Python is not
   available, write `acta.md` yourself by concatenating the phase files in order under the headings listed in the
   protocol.
3. Post a short update in the chat: two to six lines saying what happened and what each advisor holds.

At the end of phase 5 and phase 7, show the acta to the user: publish or open it if a tool for that is available
(for example an artifact or file-preview tool), otherwise give its location.

The files written by the advisors are the record. Never edit them afterwards; corrections go in later phases.

## The moderator's neutrality contract

- The moderator has **no strategy of its own**. It restates, gathers facts, integrates, and points out
  contradictions, missing facts or unclear claims. It may ask an advisor to clarify.
- **Never average.** "Half and half" is not a synthesis. A point is settled when one argument wins on the evidence,
  when both accept a third option, or when an experiment is defined to decide it.
- **Never invent agreement.** If an advisor did not accept something, it stays as an open disagreement.
- **Attribute.** In the joint strategy every move says where it comes from, and the "how they got here" section
  shows what changed and why.
- **Carry facts and assumptions through.** The joint strategy lists the assumptions it rests on and which to verify
  first.
- The user decides. Open disagreements are presented as decisions for the user, with both positions and a
  recommendation of how to settle each.

## Single-context mode (fallback)

When the advisors cannot run as separate agents, read `agents/focus.md` and `agents/sian.md` in full and write
each advisor's files yourself, strictly in role and following each system prompt. In phase 2 write Sian's
strategy first, save it, then write Focus's without revising Sian's. Mark `"mode": "single-context"` in
`meta.json`; the acta then shows that the two strategies were not produced independently. Tell the user once.

## Resuming a debate

When the user returns to an existing debate ("approve it", "change point 3", "give me the prompt"), find the
debate folder (the most recent one, or the one the user names), read `meta.json` and continue from the recorded
phase. Rebuild the acta after any change.

## Failure handling

- If an advisor returns without writing its file, send the instruction once more. If it fails again, write a file
  that says "[not produced]" and why, continue, and mention it to the user.
- If a document cannot be read, list it in the brief as unread and say so.
- Keep going when the user is away: skip phase 1, record the assumptions, run through phase 5 and stop at phase 6.
  The approval always waits for the user.
