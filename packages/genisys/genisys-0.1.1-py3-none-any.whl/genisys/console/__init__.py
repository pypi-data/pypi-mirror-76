import pkg_resources

import click


__doc__ = """
    This contains all the command line logic for Genisys, providing several functionalities:
    
        1. Installation: Enables the user to easily install and update Genisys plugin packages.
        2. Initialisation: Enables the user to initialise a Genisys package and utilise other plugins to populate it.
        3. Workspace: Creates a Genisys workspace
        4. Loads the command line interface of other Genisys plugins
    
    Args:
        genisys_cli (click.Group): Primary invoke collection for Genisys command line
    
    Todo:
        1. Create a Genisys workspace
"""


__all__ = ['genisys_cli', 'import_cli_plugins']


@click.group('genisys')
def genisys_cli() -> None:
    """
    Genisys Command Line Interface
    \f
    Returns:
        None
    """


def import_cli_plugins(cli: click.Group, entry_point: str = 'genisys.cli') -> click.Group:
    """
    Imports the command line interfaces of all Genisys plugins into the system

    Args:
        cli (click.Group): Click command line interface
        entry_point (str): User specified entry point to load plugins, defaults to 'genisys.cli'

    Returns:
        click.Group: Genisys' command line interface with plugin interfaces attached
    """
    for entry_point in pkg_resources.iter_entry_points(entry_point):
        cli.add_command(cmd=entry_point.load(), name=entry_point.name)

    return cli


genisys_cli = import_cli_plugins(genisys_cli)
