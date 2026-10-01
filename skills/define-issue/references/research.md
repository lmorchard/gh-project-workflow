# Research the current code

Use this guide when issue definition requires code investigation. You can do the investigation directly or give these instructions to a research agent. A separate agent is optional.

## Research questions

Ask how the current code behaves, rather than how to implement the desired feature. Select questions that affect the issue. Do not require a fixed number of questions.

Useful questions include:

- Which code handles the relevant input and produces the result?
- Which tests assess that behavior, and what do their assertions establish?
- Which other callers use the same code?
- Which existing tools can demonstrate the reported problem?

## Research result

Describe current behavior before proposing changes. Keep recommendations outside the factual research result. Give file and line references for claims about code.

If a search finds no implementation, name the searched locations. Do not treat a limited search as proof of absence everywhere. State which facts remain uncertain.

Describe existing tests separately from proposed tests. Record commands that you execute and their results. If you only read the code, say so.

Return answers to the requested questions with sources and relevant limits. Keep the result short enough for the issue author to use. The issue author decides scope and asks the user about unresolved choices.
