"""Command-line interface for makefolio."""

import os
import sys
from pathlib import Path

import click

from makefolio.builder import Builder
from makefolio.server import DevServer
from makefolio.utils import init_project, create_content_file


@click.group()
@click.version_option()
def main():
    """makefolio - A modern static site generator for portfolios."""
    pass


@main.command()
@click.argument("name", required=False)
@click.option(
    "--path",
    "-p",
    default=".",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Directory to initialize the project in",
)
def init(name, path):
    """Initialize a new makefolio project."""
    target_dir = Path(path)
    if name:
        target_dir = target_dir / name

    if target_dir.exists() and any(target_dir.iterdir()):
        click.echo(f"Error: Directory {target_dir} is not empty", err=True)
        sys.exit(1)

    init_project(target_dir)
    click.echo(f"✓ Created new makefolio project at {target_dir}")
    click.echo(f"\nNext steps:")
    click.echo(f"  cd {target_dir}")
    click.echo(f"  makefolio build")
    click.echo(f"  makefolio serve")


@main.command()
@click.option(
    "--source",
    "-s",
    default=".",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Source directory",
)
@click.option(
    "--output",
    "-o",
    default="build",
    help="Output directory",
)
def build(source, output):
    """Build the static site."""
    source_path = Path(source)
    output_path = source_path / output

    click.echo(f"Building site from {source_path}...")
    builder = Builder(source_path, output_path)
    builder.build()
    click.echo(f"✓ Site built successfully in {output_path}")


@main.command()
@click.option(
    "--source",
    "-s",
    default=".",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Source directory",
)
@click.option(
    "--port",
    "-p",
    default=8000,
    type=int,
    help="Port to serve on",
)
@click.option(
    "--host",
    "-h",
    default="127.0.0.1",
    help="Host to bind to",
)
def serve(source, port, host):
    """Start a development server with hot reload."""
    source_path = Path(source)
    output_path = source_path / "build"

    server = DevServer(source_path, output_path, host, port)
    server.serve()


@main.command()
@click.argument("type", type=click.Choice(["project", "page", "post", "experience", "education"]))
@click.option(
    "--name",
    "-n",
    help="Name of the content file (without extension)",
)
@click.option(
    "--source",
    "-s",
    default=".",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Source directory",
)
def new(type, name, source):
    """Create a new content file."""
    source_path = Path(source)
    content_path = create_content_file(source_path, type, name)
    click.echo(f"✓ Created {content_path}")
