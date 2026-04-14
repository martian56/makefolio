"""Content parsing and site configuration."""

import math
from pathlib import Path
from typing import Any

import frontmatter
import markdown
import yaml

WORDS_PER_MINUTE = 200


class ContentParser:
    """Parse markdown files with frontmatter into renderable content."""

    def __init__(self):
        self.md = markdown.Markdown(extensions=["fenced_code", "tables", "codehilite"])

    def parse_file(self, file_path: Path) -> dict[str, Any]:
        with open(file_path, encoding="utf-8") as f:
            post = frontmatter.load(f)

        html_content = self.md.convert(post.content)
        self.md.reset()

        word_count = len(post.content.split())
        reading_time = max(1, math.ceil(word_count / WORDS_PER_MINUTE))

        return {
            "content": html_content,
            "markdown": post.content,
            "meta": post.metadata,
            "path": file_path,
            "slug": file_path.stem,
            "word_count": word_count,
            "reading_time": reading_time,
        }

    def parse_directory(self, dir_path: Path) -> list[dict[str, Any]]:
        items = []
        if not dir_path.exists():
            return items

        for file_path in sorted(dir_path.glob("*.md"), reverse=True):
            try:
                items.append(self.parse_file(file_path))
            except Exception as e:
                print(f"Warning: Failed to parse {file_path}: {e}")

        return items

    @staticmethod
    def collect_tags(items: list[dict[str, Any]]) -> list[str]:
        """Collect and deduplicate tags across a list of content items."""
        seen: set[str] = set()
        tags: list[str] = []
        for item in items:
            for tag in item.get("meta", {}).get("tags", []):
                lower = tag.lower()
                if lower not in seen:
                    seen.add(lower)
                    tags.append(tag)
        tags.sort(key=str.lower)
        return tags


class SiteConfig:
    """Load and manage site configuration from YAML."""

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.data = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        if not self.config_path.exists():
            return {}

        with open(self.config_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value

    def __getitem__(self, key: str) -> Any:
        return self.get(key)
