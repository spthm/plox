.PHONY: fmt
fmt:
	-poetry run isort src/ tests/
	-poetry run black src/ tests/

.PHONY: lint
lint:
	-poetry run pre-commit run --all-files
	-poetry run pylint src/ tests/
	-poetry run mypy src/ tests/

.PHONY: test
test:
	poetry run tox

.PHONY: update
update:
	poetry update
	poetry run pre-commit autoupdate
