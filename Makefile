PYTHONPATH := .

test:
	@PYTHONPATH=$(PYTHONPATH) pytest -v

unit_test:
	@PYTHONPATH=$(PYTHONPATH) pytest -v -m "not perf"

perf_test:
	@PYTHONPATH=$(PYTHONPATH) pytest -v -m "perf"

coverage:
	@PYTHONPATH=$(PYTHONPATH) coverage run -m pytest && coverage report -m

lint:
	@ruff check

doc:
	@pdoc --html --force --output-dir docs .
