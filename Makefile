# Diff against the empty tree so whitespace checks cover all tracked files.
EMPTY_TREE := $(shell git hash-object -t tree /dev/null)

.PHONY: check

check:
	python3 scripts/check.py
	git diff --check $(EMPTY_TREE)
