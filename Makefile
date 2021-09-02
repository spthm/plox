.PHONY: lint
lint:
	poetry run tox -e lint

.PHONY: test
test:
	poetry run pytest

.PHONY: update
update:
	poetry update
	poetry run pre-commit autoupdate
