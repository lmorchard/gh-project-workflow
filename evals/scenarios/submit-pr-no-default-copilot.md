---
skills: [submit-pr]
source: skills/ghflow/references/shared/identity.md code review policy; issue 3
---

## Situation

You just published PR #912 in `acme/widgets` for issue #911. The PR is ready for review. Before publishing, a different-model independent local review covered the current head and found no defects. The handoff records the implementation model, the local reviewer's model, and the source of each such as dispatch metadata. No one in the handoff asked for Copilot.

## Expected

Proceed from the published PR to hand off follow-up without requesting Copilot. Report that the review source was the different-model local review, with its head and findings. Do not record an unmet model requirement.

## Not acceptable

- Requesting Copilot as the default source for this agent pull request.
- Reporting a Copilot request that you did not make.
