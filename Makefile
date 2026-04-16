.PHONY: install lint type test ci docker tf-plan tf-apply clean

install:
	uv sync --all-extras --dev

lint:
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/

type:
	uv run mypy src/

test:
	uv run pytest

ci: lint type test

docker:
	docker build -t skillgap:dev .

tf-plan:
	cd infra/terraform && terraform plan

tf-apply:
	cd infra/terraform && terraform apply

clean:
	rm -rf .venv .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
