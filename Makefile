install:
	uv sync

run:
	uv run python pac-man.py config.json

debug:
	uv run python -m pdb python pac-man.py config.json

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +

lint:
	uv run flake8 . --exclude .venv
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

test:
	uv run pytest

.PHONY: install run debug clean lint test
