# Diff against the empty tree so whitespace checks cover all tracked files.
EMPTY_TREE := $(shell git hash-object -t tree /dev/null)

.PHONY: check test

check: test
	python3 scripts/check.py
	git diff --check $(EMPTY_TREE)

test:
	python3 -m unittest discover -s cli
