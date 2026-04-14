# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

makefolio is a Python static site generator for professional portfolio websites. It processes Markdown content with YAML frontmatter into HTML using Jinja2 templates and a theme system.

## Commands

```bash
# Install for development
uv pip install -e ".[dev]"

# Build the package
uv run python -m build

# Lint & format (Ruff, line-length 100, target py311)
uv run ruff format --check src/
uv run ruff format src/      # auto-fix
uv run ruff check src/
uv run ruff check --fix src/ # auto-fix

# Type check (ty)
uv run ty check src/

# Run tests
uv run pytest --cov=src/makefolio --cov-report=term

# CLI usage (after install)
uv run makefolio init my-portfolio
uv run makefolio build
uv run makefolio serve
uv run makefolio new project --name my-project
```

## Architecture

The package lives in `src/makefolio/` with a Click-based CLI as the entry point:

- **cli.py** — Click commands: `init`, `build`, `serve`, `new`. Entry point registered as `makefolio` console script.
- **builder.py** — `Builder` class orchestrates the build pipeline: loads config, parses all content directories (projects, experience, education, pages), sets up Jinja2 with theme templates, and renders everything to `build/`.
- **content.py** — `ContentParser` parses Markdown+frontmatter files via `python-frontmatter` and `markdown` libraries. `SiteConfig` loads `config.yaml`.
- **server.py** — `DevServer` runs a threaded HTTP server with watchdog-based file watching for hot reload. Handles clean URL routing (extensionless paths → `.html`).
- **utils.py** — `init_project()` scaffolds new projects with directory structure, default config, and theme. `create_content_file()` generates content files with type-specific frontmatter templates.
- **themes/default/** — Bundled theme with Jinja2 templates and static assets (CSS/JS). Falls back to package-bundled theme if not found in the project directory.

### Content Model

A portfolio site has four content types, each in its own subdirectory under `content/`:
- `projects/` — portfolio project entries
- `experience/` — work experience items (sorted by `start_date` descending)
- `education/` — education items (sorted by `start_date` descending)
- Root `content/*.md` — standalone pages (e.g., `about.md`)

Site-wide configuration lives in `content/config.yaml` (site metadata, social links, skills, navigation).

### Build Output

`Builder.build()` wipes and recreates the `build/` directory, copies static assets from both the project and theme, then renders all templates with a unified context containing all parsed content.

## Workflow

- Always commit changes when a task is complete. Group related changes into logical commits rather than one large commit.
- Follow Conventional Commits: `feat:`, `fix:`, `refactor:`, `style:`, `docs:`, `chore:`, `test:`, `ci:`, `perf:`. Use a scope when helpful, e.g. `feat(templates): add scroll-reveal animations`.
