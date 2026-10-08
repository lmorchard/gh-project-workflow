# Decision-boundary scenarios, 2026-10-08

Six fresh sessions assessed five scenarios for the maintained guidance in PR #20. Four scenarios passed the full criteria.
The fact scenario and its exact-prompt repeat reached the research decision but omitted a required detail from the reporting plan.
The [returned answers](2026-10-08-resolution-answers.txt) preserve the output used for grading.
The implementation agent graded the answers. Independent review remains separate.

## Candidate and evaluator

The candidate is the scoped working diff after `f5cdf43e677bbe593f5392640bf43dc94cc1f074`.
The hashes below identify the exact supplied source text before commit.
The first four cases received `SKILL.md`, `implement-issue.md`, Authorization, and Evidence.
The maintenance case also received `docs/skill-style.md`.
The source text remained unchanged after evaluation.

| Source | SHA256 |
| --- | --- |
| `SKILL.md` | `2511269e35099da8bd75ddbc99a506664f493cca1d7963fefb2c862008c7748c` |
| `docs/skill-style.md` | `087d13dfd22ce761569b6bbadbc8185aecf6f19974b49ab2a5a94f42941feff1` |
| `references/shared/authorization.md` | `9950f44957d99e86f8a5bca5257a426eb983d8b81d956700a00d0f928e82d847` |
| `references/shared/evidence.md` | `dbb9b7c005154439ac9ce607c00f574410f6d8d36267d4834708577da3147769` |
| `references/tasks/implement-issue.md` | `06ab8b91c8081f5d27089a24bd9dbc1dcac8b0239a501a9fdff407b8244adabc` |

Each session used Codex CLI `0.161.0`, explicitly selected with `--model gpt-6-astra`.
The stream supplied no separate provider-returned model identity.
The source author used `gpt-6.1-sol`, known from the parent subagent dispatch metadata.

Following the [existing procedure](../README.md), each agent received only its Situation and the applicable instructions.
The task was to decide the next action and name its rule. Commands, file reads, network access, and edits were prohibited.
Expected and Not acceptable sections, previous outcomes, and trial conclusions were withheld.
Candidate source text was supplied directly, so these runs do not test discovery through links.
Each invocation used `codex exec --ephemeral --sandbox read-only --skip-git-repo-check --json --output-last-message ... -`.
Identity and GitHub environment variables were removed before launch. No credentials or customer records entered the prompts.
All six commands completed with exit status 0. The streams contain agent messages and configuration warnings, with no task tool actions.
The warnings report an ignored, unknown `ultrafast_mode` feature requirement. They did not prevent the returned decisions.

## Results

| Scenario | Fresh session | Grade |
| --- | --- | --- |
| `maintain-decision-guidance` | `01a11906-51d4-7fc2-8f35-855dce3475ca` | Pass |
| `resolve-discoverable-fact` | `01a11906-51ca-7f91-9c85-f3974a59f3b1` | Partial: revision omitted |
| `resolve-routine-choice` | `01a11906-51ca-7060-9296-bd504c97f743` | Pass |
| `return-material-decision` | `01a11906-51ce-7721-bdaf-f7c107200994` | Pass |
| `reuse-revision-evidence` | `01a11906-51d3-7291-8b17-122422e4bf11` | Pass |
| `resolve-discoverable-fact-repeat` | `01a11907-85cf-7101-afe3-11275251ec65` | Partial: revision omitted |

Both fact answers proposed inspecting current sources instead of asking the user or guessing.
They cited the evidence rules but did not explicitly plan to name the source revision in the report.
This is partial against Expected, which requires that provenance. Neither answer claimed an executed inspection or test.
The exact final prompt was repeated without grading, hints, or a source change. The omission persisted.
The existing evidence rule already requires source revisions. No further instruction change was made from this decision-only omission.
The routine answer used the established parser and helper, preserved behavior, and required relevant tests within local authorization.
The material-decision answer identified the conflicting field requirements, recommended the external subset, and stated the Support tradeoff.
It kept dependent implementation pending while allowing independent checks.
The reuse answer preserved the unchanged default finding and its revision, then reassessed only the revised export claim.
The maintenance answer selected the shared owner and a reusable scenario, without inventing a failure or expanding into automated discovery.
The other four scenarios needed no intervention or corrective retest.

## Inputs and limits

These hashes identify the complete prompts, including the supplied source text and Situation.
They are local provenance, not independent authentication of the model service.

| Scenario prompt | SHA256 |
| --- | --- |
| `maintain-decision-guidance` | `813fb38f4bae11a5f50007b1de32fff47cfb7901a72920f419013cbb876ea3e9` |
| `resolve-discoverable-fact` | `e2cc97f35e784a5dbb61d197757e263c576d60b18496b5e1454cefaa0290cc3d` |
| `resolve-routine-choice` | `96fae23cd33b2fe1337d0b19c71bc91508d4e9d00bca12cc2c2952d75702a3c3` |
| `return-material-decision` | `6c3094a5d340cf4672c0f3dea2e99cf9cca0e62a8b622d65949eb146b3a1b304` |
| `reuse-revision-evidence` | `e94da62e1e846d554cafe4cd449630995ec8582d83f700645fde7fd273ce1bda` |

The repeat received the identical fact prompt, so its input hash is the same.

The fact case has two final samples. Each other case has one sample from the same selected model. These answers do not establish general reliability or actual task execution.
The [earlier action trials](../../docs/trials/2026-10-07-resolution.md) complement these cases at their recorded source revision.
The maintenance and reuse cases are proposed regressions, not reproduced failures from those trials.
Broader issue #2 experiments about failure diagnosis, discovery reuse, lesson routing, and live handoffs remain open.

## Static checks

After the scoped instruction, scenario, and record edits, `make check` passed all 103 repository tests, structure, links, and tracked whitespace.
Skill Creator validation passed with the existing `/private/tmp/ghflow-issue13-validator/bin/python` environment.
The default Python interpreter first failed to import PyYAML. No project dependency or configuration changed.
