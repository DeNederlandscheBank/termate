"""Console script for terminator."""
import sys
import click
import terminator
import nafigator
import stanza
from nafigator import TermElement
import nafigator

@click.command()
def main(args=None):
    """Console script for terminator."""
    click.echo("Starting cli terminator")

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
