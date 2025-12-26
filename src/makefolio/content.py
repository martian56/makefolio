"""Content parsing and management."""

import frontmatter
import markdown
from pathlib import Path
from typing import Dict, List, Any
import yaml


class ContentParser:
    """Parse markdown files with frontmatter."""

    def __init__(self):
        self.md = markdown.Markdown(extensions=["fenced_code", "tables", "codehilite"])

    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse a markdown file and return content with metadata."""
        with open(file_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        html_content = self.md.convert(post.content)
        self.md.reset()

        return {
            "content": html_content,
            "markdown": post.content,
            "meta": post.metadata,
            "path": file_path,
            "slug": file_path.stem,
        }

    def parse_directory(self, dir_path: Path) -> List[Dict[str, Any]]:
        """Parse all markdown files in a directory."""
        items = []
        if not dir_path.exists():
            return items

        for file_path in sorted(dir_path.glob("*.md"), reverse=True):
            try:
                items.append(self.parse_file(file_path))
            except Exception as e:
                print(f"Warning: Failed to parse {file_path}: {e}")

        return items


class SiteConfig:
    """Load and manage site configuration."""

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.data = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            return {}

        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
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
        """Get configuration value using bracket notation."""
        return self.get(key)
