# Issue definition trial: #843

## Assessment

Needs a scope decision, not an emit-tool interview. Recommend the auth route group as a child increment that proves the confirmed goal, leaving #843 as the full REST migration. The draft contains the question and its tradeoff. No implementation or merge authorization is inferred. Ready board status does not establish readiness: issue also carries `agent-session:needs-human`, and the acceptance comment claims more than the current tests establish.

## Actual investigation

Read the define-issue SKILL.md and linked research.md only from the workflow repository. Read target CLAUDE.md/AGENTS.md (byte-identical per cmp), issue body/comments/labels/projectItems, linked #785 body/comments, and merged PR #825/#844 bodies. Read generation, generated service, auth frontend, backend decorator/auth/routes/static mount, frontend package/tsconfig, Makefile, CI configuration, vendor build options, and relevant test assertions.

Executed read-only commands: gh issue view 843/785 with JSON fields; gh pr view 825/844; gh api repos/lmorchard/decafclaw/commits/main --jq .sha; git rev-parse HEAD; git status --short; rg searches; cat/sed file reads; cmp instruction files. Local HEAD and remote main both returned 41811db089682a2952aa9573efeedfa263a3b05a. Git status returned no changes. Used remote API comparison instead of git fetch because the trial prohibits git-ref writes.

No test suite, generation, build, browser, package installation, mutation probe, or CI job log was executed/read. In particular, did not run test_api_codegen because it invokes generation and writes tracked application outputs. Did not run make check/check-js because install-js runs npm ci. Existing guards are inspection evidence only, not claimed passing baselines. Older PR assertions are historical reports, not newly reproduced results.

## Findings that change the draft

The issue comment says test_api_codegen asserts model-specific types; it actually checks three emitted file paths and separately prohibits client imports. Its proposed browser criterion cites a guard that passes with the client unused. The structural guard checks literal local imports for disk existence; it neither evaluates browser JavaScript nor covers bare/import-map specifiers or vendor output. Generated imports are extensionless, so plain tsc emit also needs a browser-resolution solution. The current auth client reads untyped JSON; typed generation alone cannot demonstrate frontend coupling until those actual calls migrate. CI currently invokes make check, but that target does not run API generation.

The _authenticated decorator hides handler signatures behind wrapper(request). Auth is a useful small first group, but does not exercise that decorator. This limitation is explicit so the slice cannot be mistaken for completing the original broad issue.

## Trial instruction observations

The skill clearly separates evidence, proposed checks, delegated questions, and default no-GitHub-write behavior. No confusing approval requirement encountered. It correctly allows tool strategy to remain an implementation choice and permits proposed new tests without treating missing existing tests as a blocker.

Repeated operations: initial gh read failed due network restriction and was retried once with escalation, successfully. Initial search assumed package.json/tsconfig.json at repo root; both were missing there, then read the actual static/ paths. Combined instruction-file read printed duplicate identical files and truncated output; targeted follow-up reads covered relevant sections/code, and cmp established identity. This is avoidable tool-output overhead, not a skill requirement. Root workspace instructions were read before target instructions; target task restrictions governed this bounded trial. No workflow docs or other trial output read.

## Limits

Did not enumerate/type every REST endpoint, audit the board, read PR diffs or all PR comments, or validate historical CI claims. Did not inspect every frontend auth event consumer or invalid JSON edge case. These are implementation investigations after scope approval, not evidence that current behavior is safe. Browser/tool availability and clean-build dependency reproducibility remain untested. No necessary source was unavailable after network escalation.

Files written only under /tmp/gh-project-workflow-trial-843. Application, project documents, GitHub and git refs unchanged.
