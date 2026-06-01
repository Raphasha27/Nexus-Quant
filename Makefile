.PHONY: install install-dev lint format test run clean

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

lint:
	ruff check api/

format:
	ruff format api/

test:
	pytest

run:
	uvicorn api.main:app --reload --port 8000

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache __pycache__ api/__pycache__
