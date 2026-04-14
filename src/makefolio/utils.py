"""Utility functions for project scaffolding and content creation."""

import shutil
from pathlib import Path
from datetime import datetime


def init_project(target_dir: Path):
    """Initialize a new makefolio project with default structure and config."""
    target_dir.mkdir(parents=True, exist_ok=True)

    (target_dir / "content").mkdir(exist_ok=True)
    (target_dir / "content" / "projects").mkdir(exist_ok=True)
    (target_dir / "content" / "experience").mkdir(exist_ok=True)
    (target_dir / "content" / "education").mkdir(exist_ok=True)
    (target_dir / "static").mkdir(exist_ok=True)
    (target_dir / "themes").mkdir(exist_ok=True)

    config_content = """# Site Configuration
site:
  title: "My Portfolio"
  description: "A professional portfolio website"
  author: "Your Name"
  url: "https://example.com"
  theme: "light"
  greeting: "Hello, I'm"
  headline: "Software Engineer"

# Social Links
social:
  github: ""
  gitlab: ""
  twitter: ""
  linkedin: ""
  email: ""
  website: ""
  medium: ""
  devto: ""
  dribbble: ""
  behance: ""
  instagram: ""
  youtube: ""
  stackoverflow: ""
  codepen: ""
  keybase: ""
  telegram: ""

# Skills
skills:
  - name: "Python"
    level: 90
  - name: "JavaScript"
    level: 85
  - name: "React"
    level: 80

# Navigation
nav:
  - name: "About"
    url: "/about"
  - name: "Projects"
    url: "/projects"
  - name: "Experience"
    url: "/experience"
  - name: "Education"
    url: "/education"
"""
    (target_dir / "content" / "config.yaml").write_text(config_content)

    about_content = """---
title: About
---

# About Me

Write about yourself here.
"""
    (target_dir / "content" / "about.md").write_text(about_content)

    theme_source = Path(__file__).parent / "themes" / "default"
    theme_target = target_dir / "themes" / "default"
    if theme_source.exists():
        shutil.copytree(theme_source, theme_target, dirs_exist_ok=True)


def create_content_file(source_path: Path, content_type: str, name: str = None) -> Path:
    """Create a new content file with frontmatter template for the given type."""
    if not name:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        name = f"{timestamp}-{content_type}"

    content_dir = source_path / "content"
    if content_type == "project":
        content_dir = content_dir / "projects"
    elif content_type == "experience":
        content_dir = content_dir / "experience"
    elif content_type == "education":
        content_dir = content_dir / "education"
    elif content_type == "post":
        content_dir = content_dir / "posts"
        content_dir.mkdir(exist_ok=True)

    content_dir.mkdir(parents=True, exist_ok=True)
    file_path = content_dir / f"{name}.md"

    if file_path.exists():
        raise FileExistsError(f"File {file_path} already exists")

    title = name.replace("-", " ").title()
    today = datetime.now().strftime("%Y-%m-%d")

    templates = {
        "project": f"""---
title: "{title}"
date: {today}
tags: []
featured: false
description: ""
---

# {title}

Project description here.

## Features

- Feature 1
- Feature 2

## Technologies

- Technology 1
- Technology 2
""",
        "experience": f"""---
title: "{title}"
company: "Company Name"
position: "Job Title"
location: "City, Country"
start_date: {today}
end_date: ""
current: true
---

# {title}

Job description and responsibilities.

## Achievements

- Achievement 1
- Achievement 2

## Technologies Used

- Technology 1
- Technology 2
""",
        "education": f"""---
title: "{title}"
institution: "University Name"
degree: "Degree Type"
field: "Field of Study"
location: "City, Country"
start_date: {today}
end_date: ""
gpa: ""
---

# {title}

Education details and achievements.

## Coursework

- Course 1
- Course 2

## Activities

- Activity 1
- Activity 2
""",
    }

    content = templates.get(
        content_type,
        f"""---
title: "{title}"
date: {today}
---

# {title}

Content here.
""",
    )

    file_path.write_text(content)
    return file_path
