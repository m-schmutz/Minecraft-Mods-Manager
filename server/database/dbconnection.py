############ Python Lib Imports ############


from sqlite3 import connect, Connection, Row


############ Project Imports ############


from server.config import DB_PATH


############ Local Imports ############


from .sql import FOREIGN_KEYS, INIT_TABLES, INSERT_MOD, SELECT_MODS_INFO, SELECT_MOD_DEPENDENCIES
from .schemas import ModsTable, DepsTable


############ DBConnection Class ############


class DBConnection:
    def __init__(self):
        # set connection to None so that context manager handles creating connection
        self.conn: Connection | None = None


    def __enter__(self):
        # connect to database
        self.conn = connect(DB_PATH)

        # activate foreign keys constraint
        self.conn.execute(FOREIGN_KEYS)

        # initialize tables if they do not exist
        self.conn.executescript(INIT_TABLES)

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


    def select_mods_info(self):
        # create cursor
        cursor = self.conn.cursor()

        # set row factory to export values with column names
        cursor.row_factory = Row

        # execute select sql
        cursor.execute(SELECT_MODS_INFO)

        # convert every row into a dictionary
        mods = [dict(row) for row in cursor.fetchall()]

        # deactivate row factory
        cursor.row_factory = None

        # go through each mod returned and get dependencies
        for mod in mods:
            # get the mod ID
            mod_id = int(mod[ModsTable.ID])

            # get the dependencies
            cursor.execute(SELECT_MOD_DEPENDENCIES, (mod_id,))
            
            # get list of dependancy names
            dep_select = cursor.fetchall()

            # convert to list of strings assign to 'dependencies
            mod[DepsTable.TABLE_NAME.lower()] = [dep[0] for dep in dep_select]

        # close the cursor
        cursor.close()

        # give list of mods a key value
        info_list = {'mods-list': mods}

        # return as dictionary
        return info_list


    def insert_mod(self, insert_params: tuple):
        # create cursor
        cursor = self.conn.cursor()

        # insert mod into the database
        cursor.execute(INSERT_MOD, insert_params)

        # close the cursor
        cursor.close()
