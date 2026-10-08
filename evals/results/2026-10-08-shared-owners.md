# Shared-reference routing, 2026-10-08

Six fresh decision-only sessions read the focused shared references through their active task links.
Five cases passed their full criteria. The subagent-question answer is partial because it omitted an explicit recommendation.
The [returned answers](2026-10-08-shared-owner-answers.txt) preserve the output used for grading.
The implementation agent graded these answers. Independent review remains separate.

## Source and method

The evaluated source commit is `f3f3a9b307327c9b00473b1e4107bfdaa5fba891`.
It includes actual `main` at `53277ca9979390dd5ace746b8084c46b17df9233`, with the merged review-preparation and parent-owned follow-up rules.
A source snapshot copied `SKILL.md`, `README.md`, every file under `references/`, and `docs/writing.md`, `docs/skill-style.md`, and `docs/direction.md`.
All 33 files matched that commit byte for byte. They remained unchanged after evaluation.

The snapshot fingerprint is `9a2a8090b6c5eae41429822ed664d9161a2f7dc69242cd0e2bbd16da36207f53`.
It hashes sorted lines of relative path, a zero byte, file SHA256, and a newline.
This is local provenance, not independent authentication of the model service.

Following the [scenario procedure](../README.md), each session received only its Situation and applicable skill paths.
A native CLI cannot load files without a tool read. These runs allowed instruction-loading reads only, then required a proposed decision.
The prompts prohibited task commands, network access, edits, dispatch, real-user questions, and reads outside the source snapshot.
Expected criteria, prior conclusions, reports, earlier outputs, and grading were withheld.
No credentials or customer data entered the prompts. Identity and GitHub environment variables were removed before launch.

Each session used Codex CLI `0.161.0` with explicit `--model gpt-6-astra` selection.
The stream supplied no separate provider-returned model identity.
The source author used `gpt-6.1-sol`, recorded from the original parent subagent dispatch.
Commands used `codex exec --ephemeral --sandbox read-only --skip-git-repo-check --json --output-last-message ... -`.
All six commands completed with exit status 0. All observed tool commands were successful `cat` reads of instructions.
Each agent loaded the new Decisions and Coordination references after reading its entry and task references.
No task action was observed. Configuration warnings reported the same ignored `ultrafast_mode` requirement as earlier sessions.

## Results

Grades use the [criteria at the evaluated commit](https://github.com/lmorchard/gh-project-workflow/tree/f3f3a9b307327c9b00473b1e4107bfdaa5fba891/evals/scenarios).

| Evaluated case | Fresh session | Grade |
| --- | --- | --- |
| `flow-continues-after-draft` | `01a119b0-a501-7bc3-9ef5-bb1c5daf3aa1` | Pass |
| `parent-external-head-update` | `01a119b0-a508-7aa3-b59e-3bd444cc389a` | Pass |
| `resolve-routine-choice` | `01a119b0-a4f5-75f2-9198-29f1018872d4` | Pass |
| `reviewer-capacity-handoff` | `01a119b0-a4f5-74c3-a978-82e004d18e98` | Pass |
| `subagent-has-question` | `01a119b0-a4fa-78c2-a224-ee767e5b8a64` | Partial: recommendation omitted |
| `submission-parent-followup` | `01a119b0-a4fd-7f21-8500-6ed93b984ec4` | Pass |

The routine answer used the existing parser and helper without an interview or broader permission.
The subagent answer returned the compatibility conflict to the parent and kept dependent changes pending.
It gave alternatives and their tradeoff but no recommended answer, so it did not satisfy the full Expected criterion.
The decision rule already requires a supported recommendation. No policy correction or corrective retest followed this proposed-plan omission.
The capacity answer preserved the established different-model path and returned dispatch to the parent without renewed approval or self-review.
The submission answer relayed the incomplete endpoint, preserved the deadline, and deferred further queue delivery until the parent returned the result.
The external-update answer notified the responsible worker and required new-head evidence and a direct final report.
The draft answer continued to authorized publication through a subagent without repeating permission or beginning implementation.

The evaluated `reviewer-capacity-handoff` input was later consolidated into the existing [capacity-limit](../scenarios/capacity-limit.md) case.
The consolidation retains the original trial source and the enriched Situation and criteria. It removes the duplicate file.
That canonical case also names `deliver-parent-issue` among its applicable skills. The evaluated session loaded `express-issue` only.
The recorded case identifier and answer remain unchanged. No policy text changed after evaluation.

## Inputs and limits

These hashes identify the complete prompts, including their source paths and ordinary Situations.

| Evaluated prompt | SHA256 |
| --- | --- |
| `flow-continues-after-draft` | `01d851a716de266c2e9dbc8a579cdf5e5d1527a5e00427b91bbe50e6ad1da183` |
| `parent-external-head-update` | `ff3a51bed3e6f07475eb41a3e421ca98568de06befd36f190fea02844e2bfe03` |
| `resolve-routine-choice` | `8d1f9bc4216de49a60a1c51986a5eb9c0e855dbbb1d23426ccfddae3de6dcbed` |
| `reviewer-capacity-handoff` | `74af64252fec3bb71f77cb3b303596cb53605d0db78ae5550ac2ff7ac01a3fba` |
| `subagent-has-question` | `97819051991d92b155bcb64ab00e3278d505f46c9f534a44b29c434b70d65e0b` |
| `submission-parent-followup` | `098f6390581df2fb9e3f59efb3f8f20b5822e0cc915c73bff000ac3e256f9529` |

Each case is one sample from one selected model. This evidence assesses instruction loading and proposed decisions, not task execution or general reliability.
The [earlier boundary grades](2026-10-08-resolution.md) remain tied to `0f2bed8`, with their original answers, hashes, and partial outcomes.
The [earlier action trials](../../docs/trials/2026-10-07-resolution.md) concern older instructions at their recorded revision.
No new live delivery, GitHub write, hosted CI run, or merge was part of these evaluations.

## Checks

The main integration and focused source changes passed all 126 repository tests, structure, links, and tracked whitespace.
Skill Creator validation passed in the existing temporary Python environment.
After the final heading and question-framing edits, affected structure, links, and whitespace checks passed.
Active root and reference anchors resolved, and source snapshot hashes matched the exact evaluated commit.
The evidence record and capacity consolidation received affected documentation and whitespace checks without another broad suite run.
