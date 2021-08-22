.PHONY: update
update:
	poetry update
	poetry run pre-commit autoupdate
