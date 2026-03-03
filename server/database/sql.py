############ Local Imports ############


from .schemas import ModsTable, DepsTable


############ FOREIGN KEYS SQL ############


FOREIGN_KEYS = 'PRAGMA foreign_keys = ON;'


############ Tables SQL ############


INIT_TABLES = f'''
CREATE TABLE IF NOT EXISTS {ModsTable.TABLE_NAME} (
    {ModsTable.ID} INTEGER PRIMARY KEY,
    {ModsTable.NAME} TEXT NOT NULL UNIQUE,
    {ModsTable.DESCRIPTION} TEXT NOT NULL,
    {ModsTable.VERSION} TEXT NOT NULL,
    {ModsTable.FILENAME} TEXT NOT NULL UNIQUE,
    {ModsTable.FILEHASH} TEXT NOT NULL UNIQUE,
    {ModsTable.LINK} TEXT NOT NULL,
    {ModsTable.TYPE} TEXT NOT NULL CHECK (type IN ('Feature', 'Library')),
    {ModsTable.ROLE} TEXT NOT NULL CHECK (role IN ('Server', 'Client', 'Client/Server'))
) STRICT; 

CREATE TABLE IF NOT EXISTS {DepsTable.TABLE_NAME} (
    {DepsTable.MOD_ID} INTEGER NOT NULL,
    {DepsTable.DEP_ID} INTEGER NOT NULL,

    FOREIGN KEY ({DepsTable.MOD_ID})
        REFERENCES {ModsTable.TABLE_NAME}({ModsTable.ID})
        ON DELETE CASCADE,

    FOREIGN KEY ({DepsTable.DEP_ID})
        REFERENCES {ModsTable.TABLE_NAME}({ModsTable.ID})
        ON DELETE RESTRICT,

    PRIMARY KEY ({DepsTable.MOD_ID}, {DepsTable.DEP_ID})
) STRICT;
'''


############ Insert SQL ############


INSERT_MOD = f'''
INSERT INTO {ModsTable.TABLE_NAME}
({ModsTable.NAME}, 
{ModsTable.DESCRIPTION}, 
{ModsTable.VERSION}, 
{ModsTable.FILENAME}, 
{ModsTable.FILEHASH}, 
{ModsTable.LINK}, 
{ModsTable.TYPE}, 
{ModsTable.ROLE})
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
'''


############ Select SQL ############


SELECT_MODS_INFO = f'''
SELECT
{ModsTable.ID},
{ModsTable.NAME}, 
{ModsTable.DESCRIPTION}, 
{ModsTable.VERSION}, 
{ModsTable.LINK}, 
{ModsTable.TYPE}, 
{ModsTable.ROLE}
FROM {ModsTable.TABLE_NAME};
'''


SELECT_MOD_DEPENDENCIES = f'''
SELECT {ModsTable.NAME}
FROM {DepsTable.TABLE_NAME}
JOIN {ModsTable.TABLE_NAME} on {ModsTable.TABLE_NAME}.{ModsTable.ID} = {DepsTable.DEP_ID}
WHERE {DepsTable.MOD_ID} = ?;
'''
