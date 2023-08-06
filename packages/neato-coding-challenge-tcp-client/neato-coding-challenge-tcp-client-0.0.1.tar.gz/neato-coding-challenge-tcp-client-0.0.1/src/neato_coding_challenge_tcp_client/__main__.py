"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Neato Coding Challenge - TCP Client."""


if __name__ == "__main__":
    main(prog_name="neato-coding-challenge-tcp-client")  # pragma: no cover
