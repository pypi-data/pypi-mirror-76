from logging import getLogger
from os.path import join

from genisys._compat import *

__doc__ = """
    A module to consolidate all Genisys related configurations stored on the Genisys workspace.
"""

__all__ = [
    # Platform
    'SYSTEM',

    # Directories
    'HOME', 'GENISYS_TMP_DIR', 'GENISYS_DIR',
    'GENISYS_BIN_DIR', 'GENISYS_CONFIG_DIR',
    'GENISYS_PLUGIN_DIR',

    # Formats
    'GENISYS_LOGGING_FORMAT', 'GENISYS_DATETIME_FORMAT'
]


logger = getLogger('genisys')


# Genisys Workspace Variables
try:
    GENISYS_BIN_DIR = join(GENISYS_DIR, 'bin')
    GENISYS_CONFIG_DIR = join(GENISYS_DIR, 'config')
    GENISYS_PLUGIN_DIR = join(GENISYS_DIR, 'packages')
except Exception:
    logger.warning('Genisys workspace has not been configured, skipping Genisys workspace imports')


# Genisys formats
GENISYS_LOGGING_FORMAT = '%(asctime)s:%(msecs)03d [%(name)s] [%(levelname)s] : %(message)s'
GENISYS_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
