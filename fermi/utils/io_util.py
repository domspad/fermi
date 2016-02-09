
from os.path import abspath, dirname, join

import fermi


_PACKAGE_PATH = dirname(abspath(fermi.__file__))


def io_pickle_file():
    """ Returns the path containing IO data files used in testing.
    """
    return join(_PACKAGE_PATH, 'database.p')