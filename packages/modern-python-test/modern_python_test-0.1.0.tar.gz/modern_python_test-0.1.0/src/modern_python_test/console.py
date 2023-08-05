# src/modern_python_test/console.py
"""Command-line interface."""
import textwrap

import click

from . import __version__, wikipedia

# API_URL: str = "https://en.wikipedia.org/api/rest_v1/page/random/summary"


@click.command()
@click.option(
    "--language",
    "-l",
    default="en",
    help="Language edition of wikipedia",
    metavar="LANG",
    show_default=True,
)
@click.version_option(version=__version__)
def main(language: str) -> None:
    """The hypermodern Python project test."""
    # with requests.get(API_URL) as response:
    #     response.raise_for_status()
    #     data = response.json()

    # data = wikipedia.random_page(language=language)

    # title = data["title"]
    # extract = data["extract"]

    # click.secho(title, fg="green")
    # click.echo(textwrap.fill(extract))

    # Using dataclases in wikipedia.py,
    # we can redo the above in 3 lines
    page = wikipedia.random_page(language=language)
    click.secho(page.title, fg="green")
    click.echo(textwrap.fill(page.extract))
