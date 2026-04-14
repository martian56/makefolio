<p align="center">
  <h1 align="center">makefolio</h1>
  <p align="center">
    <strong>A modern, fast static site generator built for professional portfolio websites.</strong>
  </p>
  <p align="center">
    Built with Python, Jinja2, and Markdown. Generates clean, responsive HTML with dark mode, scroll animations, and SEO out of the box.
  </p>
  <p align="center">
    <a href="https://pypi.org/project/makefolio/"><img src="https://img.shields.io/pypi/v/makefolio?style=flat-square&color=blue" alt="PyPI version"></a>
    <a href="https://pypi.org/project/makefolio/"><img src="https://img.shields.io/pypi/pyversions/makefolio?style=flat-square" alt="Python versions"></a>
    <a href="https://github.com/martian56/makefolio/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/martian56/makefolio/ci.yml?branch=main&style=flat-square&label=CI" alt="CI"></a>
    <a href="https://github.com/martian56/makefolio/blob/main/LICENSE"><img src="https://img.shields.io/github/license/martian56/makefolio?style=flat-square" alt="License"></a>
  </p>
</p>

---

## Features

- **Markdown + YAML frontmatter** content authoring with zero boilerplate
- **Four content types** — projects, experience, education, and standalone pages
- **Dark / Light theme** with toggle and `localStorage` persistence
- **Scroll-reveal animations** via IntersectionObserver
- **Animated skill bars** and stat counters
- **Responsive mobile menu** with hamburger toggle
- **SVG social icons** — GitHub, GitLab, LinkedIn, Twitter/X, Email, and 10+ more
- **Open Graph & Twitter Card** meta tags on every page
- **Sitemap.xml** auto-generation
- **Reading time** estimates on content pages
- **Tag collection** across projects
- **Extensible theme system** with Jinja2 templates
- **Hot-reload dev server** with file watching
- **Clean URLs** (extensionless routing)

---

## Installation

| Method | Command |
| ------ | ------- |
| pip    | `pip install makefolio` |
| [uv](https://docs.astral.sh/uv/) | `uv pip install makefolio` |
| From source | `git clone https://github.com/martian56/makefolio.git && cd makefolio && uv pip install -e ".[dev]"` |

> **Requirements:** Python 3.11+

---

## Quick Start

```bash
# 1. Scaffold a new portfolio
makefolio init my-portfolio

# 2. Enter the project directory
cd my-portfolio

# 3. Build the static site
makefolio build

# 4. Start the dev server with hot reload
makefolio serve
```

Your site is now live at `http://localhost:8000`.

---

## Creating Content

```bash
makefolio new project    --name my-project    # Portfolio project
makefolio new experience --name my-role       # Work experience entry
makefolio new education  --name my-degree     # Education entry
makefolio new page       --name contact       # Standalone page
```

Each command creates a Markdown file with the correct frontmatter template, ready to edit.

---

## Project Structure

```
my-portfolio/
├── content/
│   ├── config.yaml          # Site config, social links, skills, nav
│   ├── about.md             # Standalone pages
│   ├── projects/            # Portfolio project entries
│   ├── experience/          # Work experience (sorted by start_date)
│   └── education/           # Education entries (sorted by start_date)
├── themes/
│   └── default/
│       ├── templates/       # Jinja2 HTML templates
│       └── static/          # CSS, JS assets
├── static/                  # Custom static files (copied to build/)
└── build/                   # Generated output
```

---

## Configuration

Edit `content/config.yaml` to customize your site:

```yaml
site:
  title: "Jane Doe"
  description: "Full-Stack Engineer"
  author: "Jane Doe"
  url: "https://janedoe.dev"
  theme: "light"                # "light" or "dark" default
  greeting: "Hello, I'm"       # Hero section greeting
  headline: "Software Engineer" # Gradient text under name

social:
  github: "janedoe"
  linkedin: "janedoe"
  email: "jane@example.com"
  # twitter, gitlab, website, medium, devto, dribbble,
  # behance, instagram, youtube, stackoverflow, codepen,
  # keybase, telegram

skills:
  - name: "Python"
    level: 95
  - name: "React"
    level: 88

nav:
  - name: "About"
    url: "/about"
  - name: "Projects"
    url: "/projects"
  - name: "Experience"
    url: "/experience"
  - name: "Education"
    url: "/education"
```

---

## Content Frontmatter

<details>
<summary><strong>Project</strong> — <code>content/projects/my-project.md</code></summary>

```yaml
---
title: "My Project"
date: 2024-06-15
tags: ["python", "react", "docker"]
featured: true
description: "Short description for cards"
---

Your project write-up in Markdown...
```
</details>

<details>
<summary><strong>Experience</strong> — <code>content/experience/my-role.md</code></summary>

```yaml
---
title: "Senior Engineer"
company: "Acme Corp"
position: "Senior Engineer"
location: "Remote"
start_date: 2023-01-15
end_date: ""
current: true
---

Role description in Markdown...
```
</details>

<details>
<summary><strong>Education</strong> — <code>content/education/my-degree.md</code></summary>

```yaml
---
title: "B.Sc. Computer Science"
institution: "MIT"
degree: "Bachelor's"
field: "Computer Science"
location: "Cambridge, MA"
start_date: 2019-09-01
end_date: 2023-05-15
gpa: "3.9"
---

Additional details in Markdown...
```
</details>

---

## Built With

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Click](https://img.shields.io/badge/Click-4EAA25?style=for-the-badge&logo=python&logoColor=white)](https://click.palletsprojects.com/)
[![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white)](https://jinja.palletsprojects.com/)
[![Markdown](https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white)](https://python-markdown.github.io/)
[![YAML](https://img.shields.io/badge/YAML-CB171E?style=for-the-badge&logo=yaml&logoColor=white)](https://pyyaml.org/)
[![Watchdog](https://img.shields.io/badge/Watchdog-FF6F00?style=for-the-badge&logo=python&logoColor=white)](https://github.com/gorakhargosh/watchdog)

---

## Development

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Format (Ruff)
uv run ruff format src/

# Lint (Ruff)
uv run ruff check src/

# Type check (ty)
uv run ty check src/

# Run tests with coverage
uv run pytest --cov=src/makefolio --cov-report=term
```

---

## Contributing

Contributions are welcome! Please open an issue for bugs or feature ideas, then submit a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/my-feature`)
3. Commit your changes using [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, etc.)
4. Push to your branch and open a PR

---

## Contributors

<a href="https://github.com/martian56/makefolio/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=martian56/makefolio" />
</a>

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=martian56/makefolio&type=Date)](https://star-history.com/#martian56/makefolio&Date)

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
