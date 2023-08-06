import pkg_resources
import sys
import importlib
from typing import Any, List, Callable


__all__ = ['gimport', 'import_entry_points']


def gimport(ref: str) -> Any:
    """
    A function to abstract imports, returns a module, an object or an object's attribute referenced by a string in the
    following format:

    'module_name.module_name:object_name.object_name.attribute'

    Args:
        ref (str): String reference to be imported

    Returns:
        Any: Loaded module or object

    Raises:
        TypeError: User input is not a string
        ImportError: Unable to import given module
        LookupError: Unable to import designated object attribute within the module

    Examples:
        >>> gimport('genisys:NAME')
        >>> 'genisys'
    """
    if not isinstance(ref, str):
        raise TypeError('Invalid reference provided: {ref}'.format(ref=ref))

    module_name, sep, artifacts = ref.partition(':')
    obj = importlib.import_module(module_name)

    try:
        if artifacts:
            for name in artifacts.split('.'):
                obj = getattr(obj, name)
        return obj
    except Exception:
        raise LookupError('Unable to retrieve {artifact} from {module}'.format(artifact=artifacts, module=module_name))


def import_entry_points(module_name: str, entry_point: str, validators: List[Callable[[Any], bool]]) -> List[str]:
    """
    Imports entry points exposed in other packages and adds them to the current module calling this function, returning
    a list of all the imported items

    Args:
        module_name (str): Name of the calling module
        entry_point (str): Entry point to load
        validators (List[Callable]): Validator functions to validate the loaded entry points

    Returns:
        List[str]: List of items imported
    """

    module = sys.modules[module_name]
    imports: List[str] = []
    for ep in pkg_resources.iter_entry_points(entry_point):
        entry_point = ep.load()
        if all(validator(entry_point) for validator in validators):
            setattr(module, entry_point.__name__, entry_point)
            imports.append(entry_point.__name__)

    return imports
