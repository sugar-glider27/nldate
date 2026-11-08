# Working on nldate

This project is a Python package managed with uv. Run commands from the directory containing pyproject.toml.

## Test-first workflow

I write the pytest suite in tests/ to specify the parser's behavior. Read those tests before implementing a change. Preserve their inputs and expected results unless I request a revision. When an autograder failure reveals a new case, help me capture it in a local test before fixing the implementation.

## Parser requirements

- Expose `parse(s: str, today: date | None = None) -> date` through `from nldate import parse`. Keep the implementation in main.py under src/nldate/. Re-export parse from src/nldate/__init__.py.
- Return a datetime.date object for recognized expressions. Use the supplied today as the reference for relative dates. When today is None, obtain the current date at call time.
- Raise ValueError for unrecognized inputs, including the empty string.
- Implement general parsing rules that cover the tested formats and related inputs. Use fixed reference dates in tests for relative expressions.

## Checks

Keep pytest, mypy, and ruff as development dependencies and commit uv.lock. The assignment requires at least ten passing tests. Before reporting the implementation complete, run all four checks:

```sh
uv run pytest
uv run mypy src/
uv run ruff check
uv run ruff format --check
```

## Environment

If you’re running on Linux, leave the project’s .venv untouched. Before running any uv command, set UV_PROJECT_ENVIRONMENT to a directory outside the project, such as /tmp/nldate-linux-venv. If you’re running on macOS, use the project’s .venv normally.