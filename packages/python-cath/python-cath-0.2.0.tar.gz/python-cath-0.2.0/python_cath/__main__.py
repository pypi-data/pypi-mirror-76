# type: ignore[attr-defined]

import os
import random
from enum import Enum
from typing import List, Optional

import typer
from rich.console import Console

from python_cath import __version__
from python_cath.example import hello

app = typer.Typer(
    name="python-cath", help="Cat files w/ headers", add_completion=False,
)
console = Console()


def version_callback(value: bool):
    """Prints the version of the package."""
    if value:
        console.print(
            f"[yellow]python-cath[/] version: [bold blue]{__version__}[/]"
        )
        raise typer.Exit()


def concat(file_list, output_file):
    os.system(f"head -1 {file_list[0]} > {output_file}")
    for afile in file_list:
        os.system(f"tail -n +2 {afile} >> {output_file}")


@app.command()
def main(
    file_list: List[str] = typer.Argument(...),
    output_file: str = typer.Argument(...),
):
    """Prints a greeting for a giving name."""
    concat(file_list, output_file)
