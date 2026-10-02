# Skill scenarios

These scenarios check whether an agent that reads a skill makes the decision the skill intends. Use them after you change a skill, to find rules that the change lost or made unclear. They do not replace trials on real issues.

## Scenario format

Each file in `scenarios/` describes one situation. Its frontmatter names the skills under test and the source of the scenario, such as a trial or the commit that added the rule. The body has three sections:

- **Situation** is the only text that the agent under test receives.
- **Expected** states the decision and the reasons that a correct answer contains.
- **Not acceptable** lists answers that fail, even when part of the answer is correct.

Write the situation as facts that the agent observes. Do not hint at the answer or name the rule under test. Keep the expected decision to what the current skill text requires. When a skill change alters the intended decision, update the scenario in the same commit.

## Run a scenario

Start a fresh agent with no conversation history. Give it this prompt, with the skill paths and the situation filled in:

```text
Read these skills from this repository and the shared references they link:
SKILL_PATHS

You are the agent applying them. Here is the current situation:

SITUATION

What do you do next, and why? Name the skill rule that decides it. Do not run commands or change anything.
```

Compare the answer with the Expected and Not acceptable sections. Record the scenario, skill commit, model, and result in a dated file in `results/`. An answer passes when it reaches the expected decision for the expected reasons. Note when an answer passes for a wrong reason, because that points to unclear text.

One run is a sample, not proof. When a scenario fails, run it again before you change the skill. A rule that fails repeatedly is unclear or missing.
