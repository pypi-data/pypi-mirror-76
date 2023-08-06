""" pickledb based database for storing data
int binary or json files.
the project is strongly typed so be carefull
"""

import sys
import os
import signal
from typing import Any, List
from threading import Thread
import json
import dill

from dilldb.key_string_error import KeyStringError

# pylint: disable=too-many-public-methods, no-else-return, invalid-name
class DillDB:
    """DillDB is a key value database.
    The data is stored in a pickle/dill file or
    in json format default is binary (pickle/dill) format
    """

    def __init__(self, location: str, auto_dump: bool,
                 sig: bool, _json: bool) -> None:
        '''create the Database Object and loads the data from the location
            path. If the file does not exists, then the file will be created

            Arguments:
                location(str): database file location
                auto_dump(bool): automatic data dump
                sig(bool):  signal handler
                json(bool): use json as database format
        '''
        # set location
        self.loco = os.path.expanduser(location)
        self.auto_dump = auto_dump
        self.json = _json
        self.db = {}
        # load database
        self.load()
        self.dthread = None
        if sig:
            self.sigterm_handler()

    def __getitem__(self, key: str) -> Any:
        '''Syntax sugar for :meth:`dilldb.dilldb.get()`


        Arguments:
            key(str): key for value

        Returns:
            Any: any type stored refered by the key

        '''
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> bool:
        '''Syntax sugar for :meth:`dilldb.dilldb.set()`

        Arguments:
            key(str): key to reference the value
            value(Any): arbitrary datatype

        Returns:
            (bool): is the item set?
        '''
        return self.set(key, value)

    def __delitem__(self, key: str) -> bool:
        '''Syntax sugar for :meth:`dilldb.dilldb.rem()`

        Arguments:
            key(str): key to delete the value

        Returns:
            (bool): true if the data deleted successful else false

        '''
        return self.rem(key)

    def __len__(self) -> int:
        """length of the database

        Returns:
            (int): number of keys in the database

        """
        return len(self.db)

    def __iter__(self) -> Any:
        """ iterator function

        Returns:
            (Any): return a value overwriting the db iterator

        """
        return iter(self.db)

    def sigterm_handler(self):
        '''Assigns sigterm_handler for graceful shutdown during dump()'''
        def _sigterm_handler():
            if self.dthread is not None:
                self.dthread.join()
            sys.exit(0)
        signal.signal(signal.SIGTERM, _sigterm_handler)

    def load(self) -> bool:
        ''' Loads, reloads or changes the path to the db file

        Arguments:
            location(str): file location.

        Returns:
            bool: could load?
        '''
        if os.path.exists(self.loco):
            self._loaddb()
        else:
            # database is a dict
            self.db = {}

        return True

    def dump(self) -> bool:
        '''Force dump memory db to the database file

        Returns:
            (bool): true if the data is dumped to the file

        '''

        if self.json:
            json.dump(self.db, open(self.loco, 'wt'))
            self.dthread = Thread(
                target=json.dump,
                args=(self.db, open(self.loco, 'wt')))
        else:
            with open(self.loco, 'wb') as db_file:
                dill.dump(self.db, db_file)

            self.dthread = Thread(
                target=dill.dump,
                args=(self.db, open(self.loco, 'wb')))

        self.dthread.start()
        self.dthread.join()
        return True

    def _loaddb(self):
        '''Load or reload the dill or json info from the file'''
        try:
            if self.json:
                self.db = json.load(open(self.loco, 'rt'))
            else:
                with open(self.loco, 'rb') as db_file:
                    try:
                        self.db = dill.load(db_file)
                    except EOFError:
                        self.db = {}
        except ValueError:
            # Error raised because file is empty
            if os.stat(self.loco).st_size == 0:
                self.db = {}
            else:
                raise  # File is not empty, avoid overwriting it

    def _autodumpdb(self):
        '''Write/save the json dump into the file if auto_dump is enabled'''
        if self.auto_dump:
            self.dump()

    def set(self, key: str, value: Any) -> bool:
        '''Set the str value of a key

        Arguments:
            key(str): reference value
            value(Any): any value

        Returns:
            bool: is the key string type?

        Raises:
            KeyStringError: the key is not of string type

        '''
        if isinstance(key, str):
            self.db[key] = value
            self._autodumpdb()
            return True
        else:
            raise KeyStringError()

    def get(self, key: str) -> Any:
        '''Get the value of a key

        Arguments:
            key(str): reference information

        Returns:
            Any: get the value referenced with the key value

        Raises:
            KeyError: the key is not right

        '''
        try:
            return self.db[key]
        except KeyError:
            return False

    def getall(self) -> List[str]:
        '''Return a list of all keys in db

        Returns:
            (list): get all keys of from the db

        '''
        return self.db.keys()

    def exists(self, key: str) -> bool:
        '''is the key in the data base?

        Arguments:
            key(str): reference to value

        Returns:
            (bool): true if the key is in the database
                    else false, the key is not in the database

        '''
        return key in self.db

    def rem(self, key: str) -> bool:
        '''Delete a key value pair

        Arguments:
            key(str): reference to value

        Returns:
            (bool): could the key be deleted

        '''
        # return False instead of an exception
        if not key in self.db:
            return False
        #delete value
        del self.db[key]
        self._autodumpdb()
        return True

    def totalkeys(self, key: str = None) -> int:
        '''Get a total number of keys, lists, and dicts inside the db

        Arguments:
            key(str): reference value to get the size of the underlying value.

        Returns:
            (int): if key is set then the value is the size of the value.
                   otherwise the return value us the size of the DillDB

        '''
        if key is None:
            total = len(self)
        else:
            total = len(self.db[key])

        return total

    def append(self, key: str, more: Any) -> bool:
        '''Add more to a key's value

        Arguments:
            key(str): key to refer to value
            more(Any): add more to the value refered with key

        returns:
            (bool): True if more could add to the key value

        '''
        tmp = self.db[key]
        self.db[key] = tmp + more
        self._autodumpdb()
        return True

    def lcreate(self, name: str) -> bool:
        '''Create a list, name must be str

        Arguments:
            name(str): name is key in database

        Returns:
            (bool): true it the list could created under the name

        Raises:
            KeyStringError: key is not a string.

        '''
        if isinstance(name, str):
            self.db[name] = []
            self._autodumpdb()
            return True
        else:
            raise KeyStringError()

    def ladd(self, name: str, value: Any) -> bool:
        '''Add a value to a list

        Arguments:
            name(str): reference key to list
            value(Any): value referenced with the key to store in the list

        Returns:
            (bool):

        '''
        self.db[name].append(value)
        self._autodumpdb()
        return True

    def lextend(self, name: str, seq: list) -> bool:
        '''Extend a list with a sequence

        Arguments:
            name(str): reference to list
            seq(list): list to extend to given list

        Returns:
            (bool): True if the referenced list is extended
        '''

        self.db[name].extend(seq)
        self._autodumpdb()
        return True

    def lgetall(self, name: str) -> list:
        '''Return all values in a list

        Arguments:
            name(str): name of list

        Returns:
            (list): list under referenced key

        '''
        return self.db[name]

    def lget(self, name: str, pos: int) -> Any:
        '''Return one value in a list

        Arguments:
            name(str): list name
            pos(int): element in the list

        Returns:
            (Any): value on queried position

        '''
        return self.db[name][pos]

    def lrange(self, name: str,
               start: int = None, end: int = None) -> list:
        '''Return range of values in a list

        Arguments:
            name(str): name of list
            start(int): start position
            end(int): end position

        Returns:
            (list): sublist

        '''
        return self.db[name][start:end]

    def lremlist(self, name: str) -> int:
        '''Remove a list and all of its values

        Arguments:
            name(str): name of list

        Returns:
            (int): number of deleted elements

        '''
        number = len(self.db[name])
        del self.db[name]
        self._autodumpdb()
        return number

    def lremvalue(self, name: str, value: Any) -> bool:
        '''Remove a value from a certain list

        Arguments:
            name(str): name of list
            value(Any): any object to delete in list

        Returns:
            (bool): true if the value could removed
        '''
        self.db[name].remove(value)
        self._autodumpdb()
        return True

    def lpop(self, name: str, pos: int) -> Any:
        '''get one element in list and remove that element

        Arguments:
            name(str): list name
            pos(int): position in list

        Returns:
            (Any): return the element on the queried position

        '''
        value = self.db[name][pos]
        del self.db[name][pos]
        self._autodumpdb()
        return value

    def llen(self, name: str) -> int:
        '''Returns the length of the list

        Arguments:
            name(str): name of list

        Returns:
            (int): number of elements in list

        '''
        return len(self.db[name])

    def lappend(self, name: str, pos: int, more: Any) -> bool:
        '''Add more to a value in a list

        Arguments:
            name(str): name of list
            pos(int): position in list
            more(Any): data element

        Returns:
            (bool): true if the data could be added to the list

        '''
        tmp = self.db[name][pos]
        self.db[name][pos] = tmp + more
        self._autodumpdb()
        return True

    def lexists(self, name: str, value: Any) -> bool:
        '''Determine if a value  exists in a list

        Arguments:
            name(str): list name
            value(Any): is value in list?

        Returns:
            (bool): true if the value is in the named list

        '''
        return value in self.db[name]

    def dcreate(self, name: str) -> bool:
        '''Create a dict, name must be str

        Arguments:
            name(str): name of the new dictionary

        Returns:
            (bool): true if the dictionary is available

        Raises:
            KeyStringError: name is not a string

        '''
        if isinstance(name, str):
            self.db[name] = {}
            self._autodumpdb()
            return True
        else:
            raise KeyStringError()

    def daddp(self, name: str, pair: tuple) -> bool:
        """ add an element to the database using a tuple

        Arguments:
            name(str): database name
            pair(tuple): key value pair

        Returns:
            (bool): true if tuple elements could stored in
                    database

        """
        return self.dadd(name, pair[0], pair[1])

    def dadd(self, name: str, key: str, value: Any) -> bool:
        """ add element using key and value

        Arguments:
            name(str): name of dictionary
            key(str): value
            value(Any): value to store

        Returns:
            (bool): true if value set

        """

        self.db[name][key] = value
        self._autodumpdb()
        return True

    def dget(self, name: str, key: str) -> Any:
        '''Return the value for a key in a dict

        Arguments:
            name(str): db key
            key(str): value key

        Returns:
            (Any): element stored in dictionary

        '''
        return self.db[name][key]

    def dgetall(self, name: str) -> dict:
        '''Return all key-value pairs from a dict

        Arguments:
            name(str): db key

        Returns:
            (dict): the dictionary stored under the key

        '''
        return self.db[name]

    def drem(self, name: str) -> bool:
        '''Remove a dict and all of its pairs

        Arguments:
            name(str): database key

        Returns:
            (bool): delete the dictionary with given name

        '''
        del self.db[name]
        self._autodumpdb()
        return True

    def dpop(self, name: str, key: str) -> Any:
        '''get the dictionary element and delete the element

        Arguments:
            name(str): database key
            key(str): dictionary key

        Returns:
            (Any): element after deletion

        '''
        value = self.db[name][key]
        del self.db[name][key]
        self._autodumpdb()
        return value

    def dkeys(self, name: str) -> List[str]:
        '''Return all the keys for a dict

        Arguments:
            name(str): database name of dictionary

        Returns:
            (list): list of keys

        '''
        return self.db[name].keys()

    def dvals(self, name: str) -> list:
        '''Return all the values for a dict

        Arguments:
            name(str): database name

        Returns:
            (list): list of all values

        '''
        return self.db[name].values()

    def dexists(self, name: str, key: str) -> bool:
        '''Determine if a key exists or not in a dict

        Arguments:
            name(str): database reference
            key(str): dictionary reference

        Return:
            (bool): true if key is in the requested dictionary

        '''
        return key in self.db[name]

    def dmerge(self, name1: str, name2: str) -> bool:
        '''Merge two dicts together into name1

        Arguments:
            name1(str): reference in database
            name2(str): reference in database

        Returns:
            (bool): true if the the merge was successful

        '''
        first = self.db[name1]
        second = self.db[name2]
        first.update(second)
        self._autodumpdb()
        return True

    def deldb(self) -> bool:
        '''Delete everything from the database

        Returns:
            (bool): database is empty

        '''
        self.db = {}
        self._autodumpdb()
        return True
