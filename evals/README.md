# Skill scenarios

These scenarios check whether an agent that reads a skill makes the decision the skill intends. Use them after you change a skill, to find rules that the change lost or made unclear. They do not replace trials on real issues.

[Skill evaluations](../docs/dev/skill-evaluations.md) describes when to add a scenario, how to run and grade it, and how to record the results.

## Scenario format

Each file in `scenarios/` describes one situation. Its frontmatter names the skills under test and the source of the scenario, such as a trial or the commit that added the rule. The body has three sections:

- **Situation** is the only text that the agent under test receives.
- **Expected** states the decision and the reasons that a correct answer contains.
- **Not acceptable** lists answers that fail, even when part of the answer is correct.

Write the situation as facts that the agent observes. Do not hint at the answer or name the rule under test. Keep the expected decision to what the current skill text requires. When a skill change alters the intended decision, update the scenario in the same commit.

## Run a scenario

Use `scripts/run_scenario.py` to build and run a prompt from one committed scenario. The runner reads only the Situation section and resolves `skills` task names to paths in a snapshot of the selected commit. The snapshot contains the selected task files and their recursively linked Markdown references. It excludes scenario criteria, prior results, trial records, and this evaluation guide. The runner records its source fingerprint, prompt hash, raw answers, and run details. On failure, it also records bounded, redacted stderr diagnostics in the answer and provenance files. It does not grade answers.

Preview a prompt without launching a model session:

```sh
make run-scenario ARGS="SCENARIO --runner codex --model MODEL --dry-run"
```

Run a scenario and write its answers and provenance into a new output directory:

```sh
make run-scenario ARGS="SCENARIO --runner codex --model MODEL --repeat 2 --output-dir /tmp/scenario-run"
```

Use `--runner claude` to select Claude Code. Use `--commit COMMIT` to select a source revision. The default source is `HEAD`. Review and grade the answers separately.

The runner starts each session with no prior conversation. It applies runner-specific limits and records them in `provenance.json`. Claude Code can confine file tools to the source snapshot and disable command, code, web, and agent tools. Codex uses a read-only sandbox and disables integrations, but its CLI has no tool allowlist and does not confine reads to the snapshot. In Codex runs, the prompt forbids commands and reads outside the supplied sources; provenance marks those limits as prompt-only. Both runners need network access to call their model provider. Read the recorded limits before relying on a result.

Compare the answer with the Expected and Not acceptable sections. Record the scenario, skill commit, model, and result in a dated file in `results/`. An answer passes when it reaches the expected decision for the expected reasons. Note when an answer passes for a wrong reason, because that points to unclear text.

One run is a sample, not proof. When a scenario fails, run it again before you change the skill. A rule that fails repeatedly is unclear or missing.

## Coverage index and records

The [coverage index](INDEX.md) shows the latest recorded evidence for each current scenario.
After editing scenarios or records, use `make scenario-index` to update `evals/INDEX.md`.
Use `python3 scripts/scenario_index.py --check` to make sure that the file is current.
`make check` includes this command. Invalid records, missing blocks, and unknown scenario names cause failure.

### Write a coverage record

A coverage record is a structured summary of a report.
The generator reads JSON lists in fenced `scenario-results` blocks in every Markdown file under `results/`.
JSON uses `null` for unknown values.
Each record requires these fields:

```scenario-results
[
  {
    "scenario": "implement-does-not-merge",
    "date": "2026-10-02",
    "skill_commit": "79737b3",
    "runner": null,
    "model": "Claude Sonnet",
    "grade": "Pass",
    "phase": "sample",
    "note": null,
    "order": null
  }
]
```

This example comes from [the full sweep report](results/2026-10-02-full.md).
`scenario` names a current scenario without `.md`. Other text fields accept a nonempty string or `null`.
`date` uses `YYYY-MM-DD` when the report establishes a date for the assessment. It accepts `null` when chronology is unknown.
Historical dates come from dated report headings or explicit assessment dates. A filename alone does not establish a run date.
`skill_commit` identifies evaluated source, not the commit that adds the report.
Keep a recorded abbreviated commit unchanged. For mutable source, use `null` unless recorded hashes establish a later commit with identical bytes.
Explain that later association in `note`.
`runner` identifies the execution tool. `model` records supported actor selection or runtime identity, with its evidence limit in `note`.
A parent model does not establish an actor model.
`grade` preserves human grading and batch counts, such as `Pass (2/2)`. A batch is not an individual sample.
Use separate records for different grades or phases. Use `null` for an ungraded answer.
`phase` names the assessment phase. `note` records source limits, mappings, and grade qualifications.
`order` accepts a positive integer or `null`. Use increasing values only when the report establishes an order within one scenario.
For example, baseline records use 1 and changed-skill records use 2. Equal values retain separate samples or batches.
The generator never compares order values across reports.

### Use runner provenance

Provenance records the source and method of a run.
For output from `run_scenario.py`, copy `scenario`, `source_commit`, `runner`, and `model` from `provenance.json`.
Use the UTC date from `started_at_utc` for `date`. Examine `runs` for runtime model evidence and execution failures.
Record selected and runtime model differences in `note`. Add human grades only after reading the answers and scenario criteria.
Keep the raw answers and source limits in the report. The coverage generator does not grade answers or inspect external provenance files.

### Read historical coverage

For a renamed or consolidated scenario, name its current scenario and explain the original case and changed criteria in `note`.
An unnamed ad hoc assessment remains in the original prose. It does not become a scenario record.

The index retains all records on the latest known date and undated records.
Within one report, an explicit larger `order` value replaces earlier records for that scenario.
Records with unknown order remain visible. Report names and record text supply stable display order, not run chronology.
“No recorded run” means that no report contains a structured record for the scenario. It does not prove absence of unrecorded execution.
A changed repository HEAD alone does not invalidate earlier evidence. Read source and criteria limits before comparing results.
