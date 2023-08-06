import zipfile
from contextlib import contextmanager
from os import listdir, unlink, getcwd, chdir
from os.path import join, isfile, islink, isdir, exists
from shutil import rmtree
from tempfile import mkdtemp
from typing import Dict, List

import toml
from cookiecutter.exceptions import CookiecutterException


def clear_directory(directory: str) -> None:
    """
    Clears all contents of a specified directory

    Args:
        directory (str): Path to directory

    Returns:
        None

    Raises:
        OSError: If any errors occur during processing
    """
    for filename in listdir(directory):
        file_path = join(directory, filename)

        # Clear files
        if isfile(file_path) or islink(file_path):
            unlink(file_path)

        # Clear directories
        elif isdir(file_path):
            rmtree(file_path)


@contextmanager
def cd(directory: str) -> None:
    """
    Changes the current working directory to the specified directory

    Args:
        directory (str): Path to directory

    Returns:
        None

    Raises:
         OSError: If directory does not exist
         OSError: If current working directory was deleted midway
    """
    cwd = getcwd()
    chdir(directory)
    try:
        yield None
    finally:
        chdir(cwd)


class CookiecutterContext(object):
    """
    Context Manager setting up a Cookiecutter Environment i.e. a temporary directory to unzip and extract the templates
    and clean up thereafter
    """
    def __init__(self, templates_dir, template_name, temp_dir=None):
        self.temp_dir = temp_dir
        self.templates_dir = templates_dir
        self.template_name = template_name
        self.template = None

    def __enter__(self) -> str:
        if self.temp_dir is None:
            self.temp_dir = mkdtemp()

        if not exists(self.templates_dir):
            raise CookiecutterException("Templates directory does not exist")

        if '.'.join([self.template_name, 'zip']) not in listdir(self.templates_dir):
            raise CookiecutterException("Template {} does not exist in templates directory".format(self.template_name))

        with zipfile.ZipFile(join(self.templates_dir, '.'.join([self.template_name, 'zip'])), 'r') as template:
            template.extractall(self.temp_dir)
            self.template = join(self.temp_dir, self.template_name)

        return self.template

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.temp_dir is not None:
            rmtree(self.temp_dir, ignore_errors=True)
            self.temp_dir = None


class PyProjectTomlContext(object):
    """
    Context Manager for manipulating pyproject.toml
    """

    def __init__(self, path: str):
        self.path = path
        self.pyproject_toml = {}

    def __enter__(self) -> Dict:
        with open(self.path, 'r+') as f:
            self.pyproject_toml = toml.load(f)

        return self.pyproject_toml

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.path, 'w+') as f:
            toml.dump(self.pyproject_toml, f)


class EnvironmentContext(object):
    """
    Context Manager for managing environment variables
    """

    def __init__(self, env_file: str):
        self.env_file = env_file
        self.env_data = []

    def __enter__(self) -> List[str]:
        with open(self.env_file, 'r+') as f:
            self.env_data = f.readlines()

        return self.env_data

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.env_file, 'w+') as f:
            f.writelines(self.env_data)
