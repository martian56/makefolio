"""Utility functions for makefolio."""

import shutil
from pathlib import Path
from datetime import datetime


def init_project(target_dir: Path):
    """Initialize a new makefolio project structure."""
    target_dir.mkdir(parents=True, exist_ok=True)

    # Create directory structure
    (target_dir / "content").mkdir(exist_ok=True)
    (target_dir / "content" / "projects").mkdir(exist_ok=True)
    (target_dir / "content" / "experience").mkdir(exist_ok=True)
    (target_dir / "content" / "education").mkdir(exist_ok=True)
    (target_dir / "static").mkdir(exist_ok=True)
    (target_dir / "themes").mkdir(exist_ok=True)

    # Create default config
    config_content = """# Site Configuration
site:
  title: "My Portfolio"
  description: "A professional portfolio website"
  author: "Your Name"
  url: "https://example.com"
  theme: "light"  # light or dark

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

    # Create about page
    about_content = """---
title: About
---

# About Me

Write about yourself here.
"""
    (target_dir / "content" / "about.md").write_text(about_content)

    # Copy default theme
    theme_source = Path(__file__).parent / "themes" / "default"
    theme_target = target_dir / "themes" / "default"
    if theme_source.exists():
        shutil.copytree(theme_source, theme_target, dirs_exist_ok=True)


def create_content_file(source_path: Path, content_type: str, name: str = None) -> Path:
    """Create a new content file."""
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

    # Default frontmatter based on type
    if content_type == "project":
        frontmatter = f"""---
title: "{name.replace('-', ' ').title()}"
date: {datetime.now().strftime("%Y-%m-%d")}
tags: []
featured: false
---

# {name.replace('-', ' ').title()}

Project description here.

## Features

- Feature 1
- Feature 2

## Technologies

- Technology 1
- Technology 2
"""
    elif content_type == "experience":
        frontmatter = f"""---
title: "{name.replace('-', ' ').title()}"
company: "Company Name"
position: "Job Title"
location: "City, Country"
start_date: {datetime.now().strftime("%Y-%m-%d")}
end_date: ""  # Leave empty for current position
current: true
---

# {name.replace('-', ' ').title()}

Job description and responsibilities.

## Achievements

- Achievement 1
- Achievement 2

## Technologies Used

- Technology 1
- Technology 2
"""
    elif content_type == "education":
        frontmatter = f"""---
title: "{name.replace('-', ' ').title()}"
institution: "University Name"
degree: "Degree Type"
field: "Field of Study"
location: "City, Country"
start_date: {datetime.now().strftime("%Y-%m-%d")}
end_date: ""
gpa: ""  # Optional
---

# {name.replace('-', ' ').title()}

Education details and achievements.

## Coursework

- Course 1
- Course 2

## Activities

- Activity 1
- Activity 2
"""
    else:
        frontmatter = f"""---
title: "{name.replace('-', ' ').title()}"
date: {datetime.now().strftime("%Y-%m-%d")}
---

# {name.replace('-', ' ').title()}

Content here.
"""

    file_path.write_text(frontmatter)
    return file_path
