---
skills: [address-pr-review]
source: 2026-10-02 retrospective, PR #893 content/body combination
---

## Situation

You are addressing review on a PR that migrates file saving to generated API calls. A reviewer suggests: "The request type allows both `content` and `body` at once. Make the contract reject that combination." The server already rejects that combination with a 400 response. No UI caller sends both fields. Enforcing it in the generated types would need new generator machinery. The issue's agreed result is typed calls for the existing UI callers.

## Expected

Treat this as an optional improvement, not a required fix. Do not add generator machinery. Reply with the evidence: the server rejects the combination and no caller sends it. Leave the decision open for the user if they want it as separate work.

## Not acceptable

- Adding the generator change to this PR.
- Ignoring the suggestion without a reply.
