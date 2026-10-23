FILE ?= maps/easy/03_basic_capacity.txt

install:
	uv sync

run:
	uv run main.py $(FILE)

debug:
	uv run python3 -m pdb main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
