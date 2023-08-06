import click

from genisys.console import import_cli_plugins


@click.group('deps')
def deps_cli() -> None:
    """
    Commands to install dependencies in the current environment
    \f
    Returns:
        None
    """


deps_cli = import_cli_plugins(deps_cli, 'genisys.cli.deps')
