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
	poetry run tox -q --skip-missing-interpreters=true

.PHONY: coverage
coverage:
	-poetry run tox -q --skip-missing-interpreters=true -- -q --cov --cov-config=pyproject.toml --cov-report=
	poetry run tox -q -e coverage -- combine
	poetry run tox -q -e coverage -- html
	poetry run tox -q -e coverage -- report

.PHONY: update
update:
	poetry update
	poetry run pre-commit autoupdate
