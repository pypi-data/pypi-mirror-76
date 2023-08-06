import subprocess
from os.path import exists, join, expanduser, abspath

import click

from genisys.env import SYSTEM, GENISYS_DIR
from genisys.console.env import GENISYS_DIR_VARIABLE, GENISYS_PATH_VARIABLE, GENISYS_PYTHONPATH_VARIABLE
from genisys.console.utils import EnvironmentContext


@click.group('deinit')
def deinit_cli() -> None:
    """
    Deinitialise CLI
    \f
    Returns:
        None
    """


@deinit_cli.command()
def workspace() -> None:
    """
    Deinitialises the Genisys workspace
    \f
    Returns:
        None
    """
    click.echo("Deinitialising Genisys workspace")

    if not exists(GENISYS_DIR):
        raise click.ClickException("Genisys workspace does not exist, please check GENISYS_DIR environment variable")

    if SYSTEM == 'Windows':
        pass
    elif SYSTEM == 'Darwin':
        pass
    else:
        # First we clear the folder
        click.echo("Clearing Genisys workspace")
        try:
            subprocess.check_output(['rm', '-rf', GENISYS_DIR])
        except subprocess.SubprocessError as e:
            raise click.ClickException("{}.{}".format(e.__class__.__name__, str(e)))

        # Next we clear the environment variables
        click.echo("Clearing environment variables")
        try:
            with EnvironmentContext(join(expanduser('~'), '.bash_profile')) as data:
                for var in [GENISYS_DIR_VARIABLE, GENISYS_PATH_VARIABLE, GENISYS_PYTHONPATH_VARIABLE]:
                    if var in data:
                        data.remove(var)
        except Exception as e:
            raise click.ClickException("{}.{}".format(e.__class__.__name__, str(e)))

    click.secho(f"Successfully deinitialised Genisys workspace at {abspath(GENISYS_DIR)}, ", fg='green')
    click.echo(f'Please restart your terminal or run the following command '
               f'`exec "$SHELL"` for the changes to take effect')
