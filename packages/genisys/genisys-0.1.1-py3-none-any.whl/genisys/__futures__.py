import sys
import pkg_resources


__doc__ = """
    This module contains code that enables compatibility between Python versions
"""


__all__ = [
    'python_version',
]


python_version = {
    'major': sys.version_info.major,
    'minor': sys.version_info.minor,
    'micro': sys.version_info.micro
}


def import_futures(entry_point: str = "genisys.futures") -> None:
    """
    Imports the futures of various Genisys plugins into the Genisys ecosystem

    Args:
        entry_point (str): User specified entry point to load plugin futures

    Returns:
        None

    Todo:
        * Deconflict attributes
    """
    for module_name, future_module in [
        (entry_point.name, entry_point.load()) for entry_point in pkg_resources.iter_entry_points(entry_point)
    ]:
        for attribute in future_module:
            setattr(sys.modules[__name__], attribute.__name__, attribute)


if python_version['minor'] == 6:
    # For handling Python 3.6
    pass
if python_version['minor'] == 7:
    # For handling Python 3.7
    pass
else:
    # For handling Python >3.8
    pass


import_futures()
