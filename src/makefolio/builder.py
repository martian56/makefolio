"""Site builder and renderer."""

import shutil
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, ElementTree

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

        if not self.theme_path.exists():
            self.theme_path = Path(__file__).parent / "themes" / "default"

        self.config = SiteConfig(self.content_path / "config.yaml")
        self.parser = ContentParser()

        template_dirs = [self.theme_path / "templates"]
        self.env = Environment(
            loader=FileSystemLoader([str(d) for d in template_dirs if d.exists()]),
            autoescape=select_autoescape(["html", "xml"]),
        )
        self._add_filters()

    def _add_filters(self):
        def date_filter(value, format_string="%B %Y"):
            if not value:
                return ""
            try:
                if isinstance(value, str):
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
        if self.output_path.exists():
            shutil.rmtree(self.output_path)
        self.output_path.mkdir(parents=True)

        self._copy_static_files()

        projects = self.parser.parse_directory(self.content_path / "projects")
        experience = self.parser.parse_directory(self.content_path / "experience")
        education = self.parser.parse_directory(self.content_path / "education")
        pages = self.parser.parse_directory(self.content_path)

        pages = [
            p
            for p in pages
            if p["path"].parent == self.content_path
            and p["path"].stem not in {"projects", "experience", "education"}
        ]

        experience.sort(key=lambda x: x["meta"].get("start_date", ""), reverse=True)
        education.sort(key=lambda x: x["meta"].get("start_date", ""), reverse=True)

        all_tags = ContentParser.collect_tags(projects)

        context = {
            "site": self.config.data.get("site", {}),
            "social": self.config.data.get("social", {}),
            "skills": self.config.data.get("skills", []),
            "nav": self.config.data.get("nav", []),
            "projects": projects,
            "experience": experience,
            "education": education,
            "pages": pages,
            "all_tags": all_tags,
        }

        self._render_home(context)
        self._render_projects(context)
        self._render_experience(context)
        self._render_education(context)
        self._render_pages(context)
        self._generate_sitemap(context)

    def _copy_static_files(self):
        if self.static_path.exists():
            shutil.copytree(self.static_path, self.output_path / "static", dirs_exist_ok=True)

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

    def _render_home(self, context: Dict[str, Any]):
        template = self.env.get_template("index.html")
        html = template.render(**context)
        (self.output_path / "index.html").write_text(html, encoding="utf-8")

    def _render_projects(self, context: Dict[str, Any]):
        projects_dir = self.output_path / "projects"
        projects_dir.mkdir(exist_ok=True)

        template = self.env.get_template("projects.html")
        html = template.render(**context)
        (projects_dir / "index.html").write_text(html, encoding="utf-8")

        project_template = self.env.get_template("project.html")
        for project in context["projects"]:
            project_context = {
                **context,
                "project": project,
                "page_title": project["meta"].get("title", ""),
            }
            html = project_template.render(**project_context)
            slug = project["slug"]
            (projects_dir / f"{slug}.html").write_text(html, encoding="utf-8")

    def _render_experience(self, context: Dict[str, Any]):
        experience_dir = self.output_path / "experience"
        experience_dir.mkdir(exist_ok=True)

        template = self.env.get_template("experience.html")
        html = template.render(**context)
        (experience_dir / "index.html").write_text(html, encoding="utf-8")

        exp_template = self.env.get_template("experience-item.html")
        for exp in context["experience"]:
            title = exp["meta"].get("position", exp["meta"].get("title", ""))
            exp_context = {**context, "experience": exp, "page_title": title}
            html = exp_template.render(**exp_context)
            slug = exp["slug"]
            (experience_dir / f"{slug}.html").write_text(html, encoding="utf-8")

    def _render_education(self, context: Dict[str, Any]):
        education_dir = self.output_path / "education"
        education_dir.mkdir(exist_ok=True)

        template = self.env.get_template("education.html")
        html = template.render(**context)
        (education_dir / "index.html").write_text(html, encoding="utf-8")

        edu_template = self.env.get_template("education-item.html")
        for edu in context["education"]:
            edu_context = {**context, "education": edu, "page_title": edu["meta"].get("title", "")}
            html = edu_template.render(**edu_context)
            slug = edu["slug"]
            (education_dir / f"{slug}.html").write_text(html, encoding="utf-8")

    def _render_pages(self, context: Dict[str, Any]):
        page_template = self.env.get_template("page.html")
        for page in context["pages"]:
            slug = page["slug"]
            if slug == "index" or slug == "config":
                continue
            page_context = {**context, "page": page, "page_title": page["meta"].get("title", "")}
            html = page_template.render(**page_context)
            (self.output_path / f"{slug}.html").write_text(html, encoding="utf-8")

    def _generate_sitemap(self, context: Dict[str, Any]):
        site_url = context["site"].get("url", "").rstrip("/")
        if not site_url:
            return

        urlset = Element("urlset")
        urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

        def add_url(loc: str, priority: str = "0.5"):
            url_el = SubElement(urlset, "url")
            SubElement(url_el, "loc").text = f"{site_url}{loc}"
            SubElement(url_el, "priority").text = priority

        add_url("/", "1.0")
        add_url("/projects/", "0.8")
        add_url("/experience/", "0.8")
        add_url("/education/", "0.8")

        for project in context["projects"]:
            add_url(f"/projects/{project['slug']}.html", "0.6")

        for exp in context["experience"]:
            add_url(f"/experience/{exp['slug']}.html", "0.6")

        for edu in context["education"]:
            add_url(f"/education/{edu['slug']}.html", "0.6")

        for page in context["pages"]:
            slug = page["slug"]
            if slug not in ("index", "config"):
                add_url(f"/{slug}.html", "0.5")

        tree = ElementTree(urlset)
        sitemap_path = self.output_path / "sitemap.xml"
        tree.write(str(sitemap_path), xml_declaration=True, encoding="utf-8")
