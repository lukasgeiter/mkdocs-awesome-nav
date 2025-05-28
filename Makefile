.PHONY: all help init clean test lint format type-check coverage

all: init lint type-check coverage

help:
	@echo "Available targets:"
	@echo "  init        - Init venv"
	@echo "  test        - Run all tests"
	@echo "  lint        - Run ruff linter"
	@echo "  format      - Format code with ruff"
	@echo "  type-check  - Run mypy type checking"
	@echo "  coverage    - Run tests with coverage report"
	@echo "  clean       - Remove cache files and build artifacts"
	@echo "  all         - Run lint, type-check, and test"

init:
	uv venv

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

# Run all tests
test:
	uv run pytest

# Run linter
lint:
	uv run ruff check .

# Format code
format:
	uv run ruff format .
	uv run ruff check --fix .

# Type checking
type-check:
	uv run mypy .

# Run tests with coverage
coverage:
	uv run coverage run -m pytest
	uv run coverage report
	uv run coverage html
