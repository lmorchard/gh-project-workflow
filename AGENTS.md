# Working in this repository

Read [docs/direction.md](docs/direction.md) before proposing architecture and [docs/findings.md](docs/findings.md) before porting behavior from agent-sessions.

Build bottom up. An operation or phase must be useful on its own before it becomes part of a larger workflow. A phase is a task such as defining an issue or reviewing a PR. Do not introduce a scheduler, agent runner, or phase state machine without a demonstrated need and an explicit project decision.

Keep established decisions, inherited evidence, and proposals distinguishable in documentation. Link to the source when bringing lessons or code over. The predecessor's repository instructions do not govern this repository.

Use existing git and gh capabilities where they suffice. Add a helper when it removes a repeated procedure or failure mode. Choose implementation language and command interfaces when a concrete operation gives us enough information.

## Writing

Use simple technical English in docs, skill instructions, command help, and errors. Prefer familiar words and concrete descriptions of what happens. Explain a necessary technical term when first used. Avoid invented labels and jargon that require readers to learn a project-specific vocabulary. Keep exact command names, API fields, and other technical details when they help someone do the work.

The founding discussion identified intricate jargon as a problem in agent-sessions. Do not carry that vocabulary over merely because the old project used it.
