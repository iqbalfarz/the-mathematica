# Thin wrapper over run.py (which also works on Windows without make).
PROFILE ?= draft
PY ?= python

.PHONY: doctor all test ledger voice events sfx timeline blender manim stage remotion estimate studio

all doctor test ledger voice events sfx timeline blender manim stage remotion estimate studio:
	$(PY) run.py $@ --profile $(PROFILE)
