# import re
# import subprocess
#
# import click
#
# __doc__ = """
#     This module contains all the source code pertaining to installing Genisys plugins on the Genisys command line
#     interface. A Genisys plugin has the following nomenclature: genisys-<plugin_name>
#
#     Args:
#         install_cli (click.Group): Consolidates all the invoke functions in this module
# """
#
# __all__ = ['install_cli']
#
# from click import Abort
#
#
# @click.group('install')
# def install_cli() -> None:
#     """
#     Install group of commands
#
#     Returns:
#         None
#     """
#
#
# @install_cli.command()
# @click.option('--name', '-n', type=str)
# @click.option('--options', '-n', type=str)
# def plugin(name: str, options: str) -> None:
#     """
#     Installs a Genisys plugin repository via pip
#
#     Args:
#         name (str): Name of the Genisys plugin to be installed
#         options (str): String of options to be passed to the pip command line
#
#     Returns:
#         None
#
#     Raises:
#         Exit: An error occurred during installation, stops the programme
#
#     Examples:
#         $ genisys installation.install
#
#     Todo:
#         * This can potentially be refactored as a generic pip installation command
#     """
#
#     try:
#         click.secho("Installing package {name}".format(name=name), fg='green')
#         subprocess.check_call(['pip', 'install', options, name])
#     except Exception as e:
#         click.secho(
#             "Error {e} installing package {name} with options {options}".format(
#                 e='{}.{}'.format(e.__class__.__name__, str(e)), name=name, options=options,
#             ),
#             fg='red'
#         )
#         raise Abort()
#
#
# @install_cli.command()
# def ls(context):
#     """
#     Lists all Genisys repositories installed in the current virtual environment that Genisys is installed in.
#
#     Args:
#         context (invoke.Context): Invoke Context
#
#     Returns:
#         dict: Key-value mapping of Genisys plugin and their associated versions
#
#     Raises:
#         Exit: An error occurred during installation, stops the programme
#
#     Examples:
#         $ genisys installation.list
#         $ genisys installation.ls
#     """
#     print("{c_start}Printing installed Genisys packages{c_end}".format(c_start=GREEN, c_end=NORMAL))
#     try:
#         packages, plugins = context.run('pip freeze', hide='stdout'), {}
#     except Failure as e:
#         print("{c_start}Error {e} retrieving installed packages{c_end}".format(
#             c_start=GREEN, e='{}.{}'.format(e.__class__.__name__, str(e)), c_end=NORMAL
#         ))
#         raise Exit("Package retrieval failed")
#
#     for package in list(filter(None, packages.stdout.split('\n'))):
#         package_name, version = tuple(package.split('=='))
#         if 'genisys' in package_name:
#             plugins[package_name] = version
#             print(package_name, version)
#     return plugins
#
#
# @install_cli.command()
# def search(context):
#     """
#     Lists PyPI for Genisys plugins, this requires an active connection to the Internet
#
#     Args:
#         context (invoke.Context): Invoke Context
#
#     Returns:
#         list[dict]: A list of Genisys plugins and their associated details
#
#     Raises:
#         Exit: An error occurred during installation, stops the programme
#
#     Examples:
#         $ genisys installation.search
#     """
#     pattern = re.compile('(?P<package>(G|g)enisys-?\w*).*\((?P<version>(\d*?.)+)\).*?- (?P<description>.*)')
#     print("Searching PyPI for all Genisys repositories")
#     try:
#         packages = context.run('pip search genisys', hide='stdout')
#     except Failure as e:
#         print("{c_start}Error {e} retrieving installed packages{c_end}".format(
#             c_start=GREEN, e='{}.{}'.format(e.__class__.__name__, str(e)), c_end=NORMAL
#         ))
#         raise Exit("Package retrieval failed")
#     plugins = [p.groupdict() for p in pattern.finditer(packages.stdout)]
#     for p in plugins:
#         print("Package: {package}\t|\tdescription: {description}".format(
#             package=p['package'], description=p['description']
#         ))
#     return plugins
#
#
# installation_ns = Collection('install')
# installation_ns.add_task(install_cli)
# installation_ns.add_task(search)
# installation_ns.add_task(ls)
