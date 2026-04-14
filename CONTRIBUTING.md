# Contributing to makefolio

Thank you for your interest in contributing! This guide will help you get started.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/<your-username>/makefolio.git`
3. Install dev dependencies: `uv pip install -e ".[dev]"`
4. Create a feature branch: `git checkout -b feat/my-feature`

## Development Workflow

```bash
# Format code
uv run ruff format src/

# Lint
uv run ruff check src/

# Type check
uv run ty check src/

# Run tests
uv run pytest --cov=src/makefolio --cov-report=term
```

## Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — new feature
- `fix:` — bug fix
- `docs:` — documentation only
- `style:` — formatting, no code change
- `refactor:` — code change that neither fixes a bug nor adds a feature
- `test:` — adding or updating tests
- `chore:` — maintenance tasks
- `ci:` — CI/CD changes
- `perf:` — performance improvements

Use a scope when helpful: `feat(templates): add scroll-reveal animations`

## Pull Requests

1. Ensure all checks pass (format, lint, type check, tests)
2. Keep PRs focused — one feature or fix per PR
3. Write a clear description of what changed and why
4. Link any related issues

## Reporting Bugs

Open an issue with:
- A clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS

## Feature Requests

Open an issue describing:
- The problem you're trying to solve
- Your proposed solution
- Any alternatives you've considered

## Code Style

- Line length: 100 characters
- Target: Python 3.11+
- Linter/formatter: Ruff
- Type checker: ty
