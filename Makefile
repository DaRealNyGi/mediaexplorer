.PHONY: install test health ui compile check clean

install:
	uv sync

test:
	uv run pytest -q

health:
	uv run python scripts/test.py

ui:
	uv run python ui_client/app.py

compile:
	uv run python -m py_compile ui_client/app.py

check: compile test health

clean:
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '.pytest_cache' -exec rm -rf {} +
