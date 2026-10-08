# GitHub writes

Apply these rules before changing GitHub records. [Authorization](authorization.md) determines the permitted scope.

## Create, update, and retry

Before you create something, search for an existing equivalent. On resumption, inspect the recorded URL first.

Record the URL or identifier that a write returns immediately. After a write, read the saved result back. A command's success response is not proof.

A failed or interrupted command can leave some changes complete. Read GitHub before you retry. Do not create a second item while the first result is uncertain. Retry only the steps that failed. Do not delete a successful result to undo a later failure.

Another person or process can change an item between reads. Read it again before an update and preserve changes that you did not make. If the current content differs from what you expect, investigate before you overwrite it.

Do not change accounts, credentials, subscriptions, repository settings, or protection rules to get past a permission error. Report the required action instead.
