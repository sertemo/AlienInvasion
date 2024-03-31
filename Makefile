.PHONY: lint format type-check

all: lint format type-check

lint:
	poetry run flake8 alieninvasion

format:
	poetry un black alieninvasion

type-check:
	poetry run mypy alieninvasion