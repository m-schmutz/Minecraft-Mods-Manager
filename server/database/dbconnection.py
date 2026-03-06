#################################################################
# Python Lib Imports 

from sqlite3 import connect, Connection, Row


#################################################################
# Server Imports

from server.config import DB_PATH


#################################################################
# Local Imports

from .sql import FOREIGN_KEYS, INIT_TABLES, TEMP_CHECK_TABLE
from .sql import INSERT_MOD, INSERT_DEPENDENCY, INSERT_CLIENT_MODS
from .sql import SELECT_ALL_MODS, SELECT_ONE_MOD, SELECT_MOD_DEPENDENCIES, SELECT_CLIENT_DOWNLOADS, SELECT_CLIENT_DELETES, SELECT_CLIENT_CURRENT


#################################################################
# DBConnection Class

class DBConnection:
    '''Manages connection to database defined by DB_PATH config'''

    def __init__(self, tempTable: bool = False):
        # set connection to None so that context manager handles creating connection
        self.conn: Connection | None = None

        # set if temp table should be created
        self.tempTable = tempTable


    def __enter__(self):
        # connect to database
        self.conn = connect(DB_PATH)

        # activate foreign keys constraint
        self.conn.execute(FOREIGN_KEYS)

        # initialize tables if they do not exist
        self.conn.executescript(INIT_TABLES)

        # if temporary table is requested, create
        if self.tempTable:
            self.conn.execute(TEMP_CHECK_TABLE)

        # commit changes
        self.conn.commit()

        # return DBConnection object
        return self


    def __exit__(self, exc_type, exc, tb):
        # check if exception type is none
        if exc_type is None:
            # if no exceptions, commit 
            self.conn.commit()

        else:
            # if exception occurred, rollback changes
            self.conn.rollback()

        # close connection and set to None
        self.conn.close()
        self.conn = None

    
    def insert_mod(self, insertParams: tuple[str, str, str, str, str, str, str, str]) -> None:
        '''
        Inserts a new mod row into the 'Mods' table.

        `insertParams` is a tuple of the strings that will be inserted into the 'Mods' Table

        Format: (name, description, version, filename, filehash, link, type, role)
        '''
        # create cursor for transaction
        cursor = self.conn.cursor()

        # insert the mod into the database
        cursor.execute(INSERT_MOD, insertParams)

        # close the cursor
        cursor.close()


    def insert_dependencies(self, insertParams: list[tuple[int, int]]):
        '''
        Inserts a list of dependancies into the 'Dependencies' table.

        `insertParams` is a list of tuples each containing the ID of a mod in the 'Mods' and the ID of the mod that it is dependent on

        Format: [(mod_id, dep_id), ...]
        '''
        # create cursor for transaction
        cursor = self.conn.cursor()

        # insert all dependencies into the database
        cursor.executemany(INSERT_DEPENDENCY, insertParams)

        # close the cursor
        cursor.close()


    def insert_client_mods(self, insertParams: list[tuple[str, str]]):
        '''
        Inserts a list of client mods into the 'ClientMods' temp table

        `insertParams` is a list of tuples each containing a filename and its corresponding filehash

        Format: [(filename, filehash), ...]
        '''
        # create cursor
        cursor = self.conn.cursor()

        # insert client list
        cursor.executemany(INSERT_CLIENT_MODS, insertParams)

        # close the cursor
        cursor.close()


    def select_all_mods(self) -> list[dict[str, str|int]]:
        '''
        Selects all columns from the 'Mods' table and returns them as a list of dictionaries.

        Each Dictionary represents a single mod in the table

        Data is returned in the following format::

            [
                {
                    "id": int,
                    "name": str,
                    "description": str,
                    "version": str,
                    "filename": str,
                    "filehash": str,
                    "link": str,
                    "type": str,
                    "role": str
                }
            ]
        '''
        # create cursor
        cursor = self.conn.cursor()

        # use row factory so that values are returned with their corresponding column name
        cursor.row_factory = Row

        # select all rows in the Mods table
        cursor.execute(SELECT_ALL_MODS)

        # format returned rows as a list of dictionaries mapping column names to values
        allMods: list[dict[str, str|int]] = [dict(row) for row in cursor.fetchall()]

        # close the cursor
        cursor.close()

        # return the list
        return allMods
        

    def select_single_mod(self, modId: int) -> dict[str, str|int]:
        '''
        Selects all columns for a single mod in the 'Mods' table and returns it as a single dictionary

        Data is returned in the following format::

            {
                "id": int,
                "name": str,
                "description": str,
                "version": str,
                "filename": str,
                "filehash": str,
                "link": str,
                "type": str,
                "role": str
            }
        '''
        # create cursor
        cursor = self.conn.cursor()

        # use row factory so that values are returned with their corresponding column name
        cursor.row_factory = Row

        # select single row
        cursor.execute(SELECT_ONE_MOD, (modId,))

        # convert to dictionary of column name mapped to value
        modRow = cursor.fetchone()

        # if a row is returned, convert to dict
        if modRow:
            modRow = dict(modRow)

        # close the cursor
        cursor.close()

        # return dictionary
        return modRow
    
    
    def select_mod_dependencies(self, modId: int) -> list[str]:
        '''
        Selects the display names of mods in the 'Mods' table that are a dependency of the mod ID given

        `modId` must be an integer that matches the ID of a mod in the 'Mods' table

        Data returned the following format::

            [<name_1>, ...]
        '''
        # create cursor
        cursor = self.conn.cursor()

        # select dependency list using mod ID
        cursor.execute(SELECT_MOD_DEPENDENCIES, (modId,))

        # convert to a list of strings
        depList = [mod[0] for mod in cursor.fetchall()]

        # close cursor
        cursor.close()

        # return dependency list
        return depList


    def select_client_downloads(self):
        '''
        Select all mod filenames that need to be downloaded by the client and returns them as a list of strings

        Data returned the following format::

            [<filename_1>, ...]
        '''
        # create cursor
        cursor = self.conn.cursor()

        # select all mods that are needed by the client
        cursor.execute(SELECT_CLIENT_DOWNLOADS)
        
        # convert to list of strings
        downloadList = [filename[0] for filename in cursor.fetchall()]
        
        # close the cursor
        cursor.close()

        # return the list
        return downloadList
    

    def select_client_deletes(self):
        '''
        Select all mod filenames that need to be deleted by the client and returns them as a list of strings

        Data returned the following format::

            [<filename_1>, ...]
        '''
        # create cursor
        cursor = self.conn.cursor()

        # select all mods that are out of date on the client
        cursor.execute(SELECT_CLIENT_DELETES)
        
        # convert to list of strings
        deleteList = [filename[0] for filename in cursor.fetchall()]
        
        # close the cursor
        cursor.close()

        # return the list
        return deleteList
    

    def select_client_current(self):
        '''
        Select all mod filenames that are up-to-date on the client and returns them as a list of strings

        Data returned the following format::

            [<filename_1>, ...]
        '''
        # create cursor
        cursor = self.conn.cursor()

        # select all mods that are up to date on the client
        cursor.execute(SELECT_CLIENT_CURRENT)
        
        # convert to list of strings
        currentList = [filename[0] for filename in cursor.fetchall()]
        
        # close the cursor
        cursor.close()

        # return the list
        return currentList
        