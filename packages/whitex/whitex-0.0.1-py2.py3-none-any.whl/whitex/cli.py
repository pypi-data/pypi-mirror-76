"""Console script for whitex."""
import sys
import click

from whitex.whitex import clean_buffer


@click.command()
@click.argument("input_file", type=click.File('r'))
@click.argument("output_file", type=click.File('w'))
def main(input_file, output_file):
    """Console script for whitex."""
    clean_buffer(input_file, output_file)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
