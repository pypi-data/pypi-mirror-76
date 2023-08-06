import platform
from os import getenv
from os.path import expanduser


__doc__ = """
    This module contains code that enables cross-platform interoperability.
    
    Todo:
        * Discriminate by platform type
"""

__all__ = [
    # Platform
    'SYSTEM',

    # Directories
    'HOME', 'GENISYS_TMP_DIR', 'GENISYS_DIR'
]


SYSTEM = platform.system()

if SYSTEM == 'Windows':
    # TODO: Handle Windows
    # HOME = expanduser('~')
    # GENISYS_DIR = join(HOME, '.genisys')
    pass

elif SYSTEM == 'Darwin':
    # TODO: Handle MacOS
    # HOME = expanduser('~')
    # GENISYS_DIR = join(HOME, '.genisys')
    pass

else:
    # For Linux systems
    GENISYS_TMP_DIR = '/tmp'
    HOME = expanduser('~')
    GENISYS_DIR = getenv('GENISYS_DIR')
