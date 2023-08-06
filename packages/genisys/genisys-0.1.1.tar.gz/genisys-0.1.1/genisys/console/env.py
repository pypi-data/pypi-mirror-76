from os import getenv
from os.path import abspath, dirname, join


__doc__ = """
    Constants and environment parameters for the genisys.console package
"""


# Shell
SHELL = getenv('SHELL')

# Directories
GENISYS_DIR = getenv('GENISYS_DIR')
TEMPLATES_DIR = join(dirname(abspath(__file__)), 'templates')

# Variables
GENISYS_PATH_VARIABLE = """export PATH="{directory}/bin:$PATH"\n"""
GENISYS_PYTHONPATH_VARIABLE = """export PYTHONPATH="{directory}/packages:$PYTHONPATH"\n"""
GENISYS_DIR_VARIABLE = """export GENISYS_DIR={directory}\n"""