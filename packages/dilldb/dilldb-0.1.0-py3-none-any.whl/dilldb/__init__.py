""" key value database based on pickledb """
from dilldb.dilldb import DillDB

__version__ = (0, 1, 0)
__author__ = "anton feldmann"
__email__ = "anton.feldmann@gmail.com"


def load(location: str,
         auto_dump: bool,
         sig: str = True,
         _json: bool = False) -> DillDB:
    '''Return a DillDB object.

    Attributes:
        location (string): path to the database location
        auto_dump (boolean):

    Returns:
         DillDB: DillDB Object
    '''
    return DillDB(location, auto_dump, sig, _json)


def dbmerge(first: DillDB, second: DillDB) -> bool:
    """Merge 2 Databases in the fist db

        Arguments:
            first(DillDB): database one
            second(DillDB): database two

        Returns:
            (bool): could merge the databases

        """
    first.dmerge(second.db)
    return True
