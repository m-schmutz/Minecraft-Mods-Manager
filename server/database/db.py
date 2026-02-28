from sqlite3 import connect, Connection, Row
from server.config import DB_PATH
from server.database import FOREIGN_KEYS, INIT_TABLES
from server.database.sql import INSERT_MOD, SELECT_MODS_INFO
from server.database.params import ModInsert



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


    def add_mod(self, mod_insert: ModInsert):

        params = (
            mod_insert.name,
            mod_insert.description,
            mod_insert.version,
            mod_insert.filename,
            mod_insert.filehash,
            mod_insert.link,
            mod_insert.type,
            mod_insert.role
        )

        cursor = self.conn.cursor()

        cursor.execute(INSERT_MOD, params)

        cursor.close()


    def get_mods_info(self) -> dict:
        
        self.conn.row_factory = Row
        cursor = self.conn.cursor()

        cursor.execute(SELECT_MODS_INFO)

        mods = [dict(row) for row in cursor.fetchall()]

        for mod in mods:
            mod['dependancies'] = []

        info_list = {'mod-list': mods}

        return info_list
        
    