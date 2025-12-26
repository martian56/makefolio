"""Site builder and renderer."""

import shutil
from pathlib import Path
from typing import Dict, Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from makefolio.content import ContentParser, SiteConfig


class Builder:
    """Build static site from source files."""

    def __init__(self, source_path: Path, output_path: Path):
        self.source_path = source_path
        self.output_path = output_path
        self.content_path = source_path / "content"
        self.static_path = source_path / "static"
        self.theme_path = source_path / "themes" / "default"

        # Fallback to package theme if not found
        if not self.theme_path.exists():
            self.theme_path = Path(__file__).parent / "themes" / "default"

        self.config = SiteConfig(self.content_path / "config.yaml")
        self.parser = ContentParser()

        # Setup Jinja2
        template_dirs = [self.theme_path / "templates"]
        self.env = Environment(
            loader=FileSystemLoader([str(d) for d in template_dirs if d.exists()]),
            autoescape=select_autoescape(["html", "xml"]),
        )
        self._add_filters()

    def _add_filters(self):
        """Add custom Jinja2 filters."""
        from datetime import datetime

        def date_filter(value, format_string="%B %Y"):
            """Format a date string."""
            if not value:
                return ""
            try:
                if isinstance(value, str):
                    # Try different date formats
                    for fmt in ["%Y-%m-%d", "%Y-%m", "%Y"]:
                        try:
                            dt = datetime.strptime(value, fmt)
                            break
                        except ValueError:
                            continue
                    else:
                        return value
                else:
                    dt = value
                return dt.strftime(format_string)
            except (ValueError, AttributeError):
                return value

        self.env.filters["date"] = date_filter

    def build(self):
        """Build the complete static site."""
        # Clean output directory
        if self.output_path.exists():
            shutil.rmtree(self.output_path)
        self.output_path.mkdir(parents=True)

        # Copy static files
        if self.static_path.exists():
            shutil.copytree(self.static_path, self.output_path / "static", dirs_exist_ok=True)

        # Copy theme static files
        theme_static = self.theme_path / "static"
        if theme_static.exists():
            static_dir = self.output_path / "static"
            static_dir.mkdir(exist_ok=True)
            for item in theme_static.rglob("*"):
                if item.is_file():
                    rel_path = item.relative_to(theme_static)
                    target = static_dir / rel_path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, target)

        # Parse content
        projects = self.parser.parse_directory(self.content_path / "projects")
        experience = self.parser.parse_directory(self.content_path / "experience")
        education = self.parser.parse_directory(self.content_path / "education")
        pages = self.parser.parse_directory(self.content_path)

        # Filter out special directories from pages
        exclude_dirs = {"projects", "experience", "education"}
        pages = [
            p
            for p in pages
            if p["path"].parent == self.content_path
            and p["path"].stem not in exclude_dirs
        ]

        # Sort experience and education by date (newest first)
        experience.sort(key=lambda x: x["meta"].get("start_date", ""), reverse=True)
        education.sort(key=lambda x: x["meta"].get("start_date", ""), reverse=True)

        # Build context
        context = {
            "site": self.config.data.get("site", {}),
            "social": self.config.data.get("social", {}),
            "skills": self.config.data.get("skills", []),
            "nav": self.config.data.get("nav", []),
            "projects": projects,
            "experience": experience,
            "education": education,
            "pages": pages,
        }

        # Render pages
        self._render_home(context)
        self._render_projects(context)
        self._render_experience(context)
        self._render_education(context)
        self._render_pages(context)

    def _render_home(self, context: Dict[str, Any]):
        """Render the home page."""
        template = self.env.get_template("index.html")
        html = template.render(**context)
        (self.output_path / "index.html").write_text(html, encoding="utf-8")

    def _render_projects(self, context: Dict[str, Any]):
        """Render project pages."""
        projects_dir = self.output_path / "projects"
        projects_dir.mkdir(exist_ok=True)

        # Projects listing page
        template = self.env.get_template("projects.html")
        html = template.render(**context)
        (projects_dir / "index.html").write_text(html, encoding="utf-8")

        # Individual project pages
        project_template = self.env.get_template("project.html")
        for project in context["projects"]:
            project_context = {**context, "project": project}
            html = project_template.render(**project_context)
            slug = project["slug"]
            (projects_dir / f"{slug}.html").write_text(html, encoding="utf-8")

    def _render_experience(self, context: Dict[str, Any]):
        """Render experience pages."""
        experience_dir = self.output_path / "experience"
        experience_dir.mkdir(exist_ok=True)

        # Experience listing page
        template = self.env.get_template("experience.html")
        html = template.render(**context)
        (experience_dir / "index.html").write_text(html, encoding="utf-8")

        # Individual experience pages
        exp_template = self.env.get_template("experience-item.html")
        for exp in context["experience"]:
            exp_context = {**context, "experience": exp}
            html = exp_template.render(**exp_context)
            slug = exp["slug"]
            (experience_dir / f"{slug}.html").write_text(html, encoding="utf-8")

    def _render_education(self, context: Dict[str, Any]):
        """Render education pages."""
        education_dir = self.output_path / "education"
        education_dir.mkdir(exist_ok=True)

        # Education listing page
        template = self.env.get_template("education.html")
        html = template.render(**context)
        (education_dir / "index.html").write_text(html, encoding="utf-8")

        # Individual education pages
        edu_template = self.env.get_template("education-item.html")
        for edu in context["education"]:
            edu_context = {**context, "education": edu}
            html = edu_template.render(**edu_context)
            slug = edu["slug"]
            (education_dir / f"{slug}.html").write_text(html, encoding="utf-8")

    def _render_pages(self, context: Dict[str, Any]):
        """Render content pages."""
        page_template = self.env.get_template("page.html")
        for page in context["pages"]:
            page_context = {**context, "page": page}
            html = page_template.render(**page_context)
            slug = page["slug"]
            if slug == "index":
                continue
            (self.output_path / f"{slug}.html").write_text(html, encoding="utf-8")
