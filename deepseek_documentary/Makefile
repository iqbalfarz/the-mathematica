# Pipeline: research ledger -> voice -> render scenes -> compose -> validate -> docs
QUALITY ?= preview
WORKERS ?= $(shell nproc)
PY ?= python
export PYTHONPATH := $(CURDIR)/src

.PHONY: all ledger voice render compose validate docs sheets clean-scenes

all: ledger voice render compose validate docs

ledger:
	$(PY) research/build_ledger.py

voice:
	$(PY) -m docu.narration.generate_voice

render:
	$(PY) -m docu.rendering.render --quality $(QUALITY) --workers $(WORKERS)

compose:
	$(PY) -m docu.rendering.compose --quality $(QUALITY)

validate:
	$(PY) -m docu.validation.report --quality $(QUALITY)

docs:
	$(PY) -m docu.docs --quality $(QUALITY)

sheets:
	$(PY) -m docu.validation.contact_sheet --quality $(QUALITY)

clean-scenes:
	rm -rf build/scenes/$(QUALITY)
