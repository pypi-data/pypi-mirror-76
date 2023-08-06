
from os import listdir, mkdir
from os.path import exists, join, basename, dirname
from textwrap import dedent
from typing import Tuple

import click
from cookiecutter.main import cookiecutter

from genisys.console import import_cli_plugins
from genisys.console.env import TEMPLATES_DIR
from genisys.console.utils import clear_directory, cd, CookiecutterContext, PyProjectTomlContext


__doc__ = """
    This modules allows users to create a new Genisys project directory and subsequently populate it with different
    Genisys plugins.
    
    Todo:
        * Import init command from other Genisys packages
"""


@click.group('create')
def create_cli() -> None:
    """
    Commands to create Genisys-related directories
    \f
    Returns:
        None
    """


@create_cli.command()
@click.option('--directory', '-d', type=str, default='.',
              help='User specified directory, defaults to the current directory')
@click.option('--overwrite', is_flag=True, default=False, help='Overwrites the current directory if it is populated')
def project(directory: str, overwrite: bool) -> Tuple[str, str]:
    """
    Initialises a new Genisys microservice project in the directory specified
    \f
    Args:
        directory (str): User specified directory, defaults to the current directory
        overwrite (str): Flag to overwrite the current directory

    Returns:
        Tuple[str, str]: Returns a tuple of (project_name, project_dir)

    Raises:
        click.ClickException: If task fails

    Examples:
        $ genisys init project --directory /path/to/project
    """
    click.echo("Creating Genisys project")
    try:
        # First we check if the directory exists and create it if it doesn't
        if not exists(directory):
            mkdir(directory)

        # If the directory has contents and the overwrite flag is present, we clear its contents
        if overwrite:
            clear_directory(directory)
    except OSError as e:
        raise click.ClickException("{}.{}".format(e.__class__.__name__, str(e)))

    try:
        # Next we enter the directory and begin initialising the directory as a Genisys Project
        with cd(directory):
            with CookiecutterContext(templates_dir=TEMPLATES_DIR, template_name='project') as temp_dir:
                project_dir = cookiecutter(template=temp_dir)
                click.secho('Genisys project successfully initialised at {directory}'.format(
                    directory=project_dir),
                    fg='green'
                )

        return basename(project_dir), project_dir
    except Exception as e:
        raise click.ClickException("{}.{}".format(e.__class__.__name__, str(e)))


@create_cli.command()
@click.option('--directory', '-d', type=str, default='.',
              help='User specified directory, defaults to the current directory')
@click.option('--create-project', '-c', is_flag=True, default=False,
              help='Creates a Genisys Project if the current directory is not already one')
@click.pass_context
def plugin(context: click.Context, directory: str, create_project: bool) -> Tuple[str, str]:
    """
    Initialises a new Genisys plugin in the Genisys Project directory specified
    \f
    Args:
        context (click.Context): Click Context passed into the plugin function
        directory (str): User specified directory, defaults to the current directory
        create_project (bool): Flag to indicate if a Genisys Project should be created

    Returns:
        Tuple[str, str]: Returns a tuple of (plugin_name, plugin_dir)

    Raises:
        click.ClickException: If task fails

    Examples:
        $ genisys init plugin --directory /path/to/project
    """
    def create_genisys_plugin(plugin_dir: str) -> Tuple[str, str]:
        """
        Function that creates a Genisys plugin in specified directory

        Args:
            plugin_dir (str): Directory to create plugin

        Returns:
            Tuple[str, str]: Returns a tuple of (plugin_name, plugin_dir)

        Raises:
            CookiecutterException: If template directory does not exist
            CookiecutterException: If template directory does contain plugin template
        """
        # Extracting plugin directory
        with cd(plugin_dir):
            with CookiecutterContext(templates_dir=TEMPLATES_DIR, template_name='plugin') as temp_dir:
                directory = cookiecutter(template=temp_dir)
                click.secho('Genisys plugin successfully initialised at {directory}'.format(
                    directory=directory),
                    fg='green'
                )
        plugin_name = basename(directory)

        # Updating pyproject.toml with plugin settings
        with PyProjectTomlContext(join(dirname(directory), 'pyproject.toml')) as pyproject_toml:
            pyproject_toml['tool']['poetry'].update(
                {
                    'packages': [{'include': plugin_name}],
                    'exclude': [join(plugin_name, '*', 'tests')],
                    'scripts': {},
                    'plugins': {
                        'genisys.cli': {
                            plugin_name: '{name}.console:cli'.format(name=plugin_name)
                        },
                        'genisys.cli.deps': {
                            plugin_name: '{name}.console.deps:deps_cli'.format(name=plugin_name)
                        },
                        'genisys.cli.create': {
                            plugin_name: '{name}.console.create:create_cli'.format(name=plugin_name)
                        },
                        'genisys.cli.devops': {
                            plugin_name: '{name}.console.devops:devops_cli'.format(name=plugin_name)
                        },
                        'genisys.cli.config': {
                            plugin_name: '{name}.console.config:config_cli'.format(name=plugin_name)
                        }
                    },
                }
            )
            pyproject_toml['tool'].update(
                {
                    'tox': {
                        'legacy_tox_ini': dedent(
                            f"""
                               [tox]
                               isolated_build = True
                               envlist = py36,py37,py38
                                
                               [testenv]
                               commands = python -m unittest discover -v -s ./{plugin_name} -t .
                            """
                        )
                    }
                }
            )
        return plugin_name, directory

    click.echo("Creating Genisys plugin in {directory}".format(directory=directory))
    # Check if the directory exists in the first place
    if not exists(directory):
        result = click.prompt("Directory {directory} does not exist, would you like to create it?".format(
            directory=directory),
            type=bool
        )
        if result:
            mkdir(directory)
            create_project = result
        else:
            raise click.ClickException("Unable to proceed as directory {directory} does not exist".format(
                directory=directory)
            )

    try:
        # First we must ensure that the current directory is a valid Genisys Project
        # So we compare it against the Genisys project structure
        with CookiecutterContext(templates_dir=TEMPLATES_DIR, template_name='project') as project_dir:
            project_dir_contents = listdir(join(project_dir, '{{cookiecutter.project_name}}'))
            current_dir_contents = listdir(directory)

        # If all the requirements for a Genisys Project are met, we proceed with the plugin installation
        if all(i in current_dir_contents for i in project_dir_contents):
            click.echo("Directory is a Genisys Project, will proceed with plugin installation")
            return create_genisys_plugin(directory)

        # Directory is not a Genisys Project, but user wants to create one in this folder
        elif create_project:
            click.echo("Directory is not a Genisys Project, will proceed to create one")
            project_name, project_dir = context.invoke(project, directory=directory)
            return create_genisys_plugin(project_dir)

        # Terminate
        else:
            click.secho("Unable to install plugin as {} is not a Genisys Project".format(directory), fg='red')

    except Exception as e:
        raise click.ClickException("{}.{}".format(e.__class__.__name__, str(e)))


create_cli = import_cli_plugins(create_cli, 'genisys.cli.create')
