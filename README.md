# makefolio

A modern, fast static site generator built for professional portfolio websites.

Built with Python, Jinja2, and Markdown. Generates clean, responsive HTML with dark mode, scroll animations, and SEO out of the box.

## Features

- **Markdown + Frontmatter** content authoring
- **Dark / Light theme** with toggle and `localStorage` persistence
- **Scroll-reveal animations** via IntersectionObserver
- **Animated skill bars** and stat counters
- **Responsive mobile menu** with hamburger toggle
- **SVG social icons** (GitHub, GitLab, LinkedIn, Twitter/X, Email, and more)
- **Open Graph & Twitter Card** meta tags on every page
- **Sitemap.xml** auto-generation
- **Reading time** estimates on content pages
- **Tag collection** across projects
- **Extensible theme system** with Jinja2 templates
- **Hot-reload dev server** with file watching (watchdog)
- **Clean URLs** (extensionless routing)

## Installation

```bash
pip install makefolio
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv pip install makefolio
```

## Quick Start

```bash
# Scaffold a new portfolio
makefolio init my-portfolio

# Enter the project
cd my-portfolio

# Build the static site
makefolio build

# Start the dev server with hot reload
makefolio serve
```

## Creating Content

```bash
# New project page
makefolio new project --name my-project

# New experience entry
makefolio new experience --name my-role

# New education entry
makefolio new education --name my-degree

# New standalone page
makefolio new page --name contact
```

Each command creates a Markdown file with the correct frontmatter template.

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

## Configuration

Edit `content/config.yaml`:

```yaml
site:
  title: "Jane Doe"
  description: "Full-Stack Engineer"
  author: "Jane Doe"
  url: "https://janedoe.dev"
  theme: "light"              # "light" or "dark" default
  greeting: "Hello, I'm"     # Hero section greeting
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

## Content Frontmatter

**Project** (`content/projects/my-project.md`):

```yaml
---
title: "My Project"
date: 2024-06-15
tags: ["python", "react", "docker"]
featured: true
description: "Short description for cards"
---
```

**Experience** (`content/experience/my-role.md`):

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
```

**Education** (`content/education/my-degree.md`):

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
```

## Development

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run linter
uv run black --check src/

# Run tests
uv run pytest --cov=src/makefolio
```

## License

MIT
