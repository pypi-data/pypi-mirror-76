import subprocess
from os import getcwd
from os.path import expanduser, exists, join, abspath

import click
from cookiecutter.main import cookiecutter

from genisys.env import SYSTEM
from genisys.console.env import TEMPLATES_DIR, GENISYS_DIR_VARIABLE, GENISYS_PYTHONPATH_VARIABLE, GENISYS_PATH_VARIABLE
from genisys.console.utils import CookiecutterContext, cd, EnvironmentContext


@click.group('init')
def init_cli() -> None:
    """
    Commands to setup and initialise Genisys in the current environment
    \f
    Returns:
        None
    """


@init_cli.command()
@click.option('--directory', '-d', type=str, default=expanduser('~/.genisys'),
              help='User specified directory, defaults to $HOME/.genisys')
@click.option('--version', '-v', type=str, default='', help='Version of Genisys to be installed')
def workspace(directory: str, version: str) -> None:
    """
    Initialises a new Genisys workspace in the directory specified
    \f
    Args:
        directory (str): Directory to initialise the Genisys workspace
        version (str): Version of Genisys to be installed

    Returns:
        None

    Raises:
        click.ClickException: If directory already exists

    Examples:
        $ genisys init workspace --directory /path/to/workspace

    Todo:
        * Setup workspace for Windows
        * Setup workspace for MacOS
        * Set environment variables for zsh terminal (.zshrc)
        * Set environment variables for fish terminal (fish -c set -U fish_user_paths {} $fish_user_paths)
    """
    click.echo("Creating Genisys workspace")

    if SYSTEM == 'Windows':
        pass
    elif SYSTEM == 'Darwin':
        pass
    else:
        click.echo("Linux environment detected, creating Genisys workspace in Linux Environment")

        # First we validate if the directory already exists
        if exists(directory):
            raise click.ClickException("Directory already exists")

        # Then we create an isolated environment to extract the workspace template
        click.echo("Setting up workspace")
        try:
            with CookiecutterContext(templates_dir=TEMPLATES_DIR, template_name='workspace') as temp_dir:

                # Here we install the template with cookiecutter
                click.secho('Genisys workspace successfully initialised at {}'.format(
                    cookiecutter(template=temp_dir, no_input=True, extra_context={'genisys_dir': directory})),
                    fg='green'
                )
        except Exception as e:
            raise click.ClickException("{}.{}".format(e.__class__.__name__, str(e)))

        # Next we install the required version of Genisys
        try:
            click.echo('Installing Genisys into workspace')
            with cd(directory):
                subprocess.check_output(
                    ['pip', 'install', '-U', 'genisys=={}'.format(version) if version else 'genisys',
                     '--ignore-installed',
                     '--install-option='
                     f'"--install-scripts={getcwd()}/bin '
                     f'--prefix={getcwd()}/packages"'],
                    stderr=subprocess.STDOUT
                )
        except Exception as e:
            raise click.ClickException("{}.{}".format(e.__class__.__name__, str(e)))

        # Next we set Environment variables
        try:
            click.echo('Setting Environment variables')
            with EnvironmentContext(join(expanduser('~'), '.bash_profile')) as data:
                data.append(GENISYS_DIR_VARIABLE.format(directory=abspath(directory)))
                data.append(GENISYS_PYTHONPATH_VARIABLE.format(directory=abspath(directory)))
                data.append(GENISYS_PATH_VARIABLE.format(directory=abspath(directory)))
        except Exception as e:
            raise click.ClickException("{}.{}".format(e.__class__.__name__, str(e)))

    click.secho(f"Successfully created Genisys workspace at {abspath(directory)}, ", fg='green')
    click.echo(f'Please restart your terminal or run the following command '
               f'`exec "$SHELL"` for the changes to take effect')
