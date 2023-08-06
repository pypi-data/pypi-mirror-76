
from typing import Dict, Tuple, Any

__all__ = ['merge_dicts']


def merge_dicts(*dicts: Tuple[Any, Dict[str, Any]]) -> Dict:
    """
    Merges dictionaries together into a single one with the last one taking precedence

    Args:
        dicts (Sequence[Dict]): Sequence of dictionaries to be merged

    Return:
        Dict: Merged dictionary
    """
    result: Dict = {}
    for d in dicts:
        result.update(d)
    return result
