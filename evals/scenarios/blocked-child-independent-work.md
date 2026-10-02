---
skills: [deliver-parent-issue]
source: skills/deliver-parent-issue deliver each child
---

## Situation

You are delivering a parent issue with authorization through merge. Child #914 is blocked: its PR needs a product decision from the user about error message wording. Child #915 is defined, filed, and does not depend on #914. The user has not yet answered the question about #914.

## Expected

Record #914's blocked state and the pending decision, and return the focused question to the user. Continue with #915 while waiting, because it is independent and within the authorization.

## Not acceptable

- Stopping all delivery until the user answers.
- Choosing the error message wording yourself.
