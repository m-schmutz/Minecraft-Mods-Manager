#################################################################
# Local Imports

from .schemas import ModsTable, DepsTable, ClientMods
from .schemas import TypeValues, RoleValues


#################################################################
# SQL to activate foreign keys

FOREIGN_KEYS = 'PRAGMA foreign_keys = ON;'


#################################################################
# SQL for creating tables

INIT_TABLES = f'''
CREATE TABLE IF NOT EXISTS {ModsTable.TABLE_NAME} (
    {ModsTable.ID} INTEGER PRIMARY KEY,
    {ModsTable.NAME} TEXT NOT NULL UNIQUE,
    {ModsTable.DESCRIPTION} TEXT NOT NULL,
    {ModsTable.VERSION} TEXT NOT NULL,
    {ModsTable.FILENAME} TEXT NOT NULL UNIQUE,
    {ModsTable.FILEHASH} TEXT NOT NULL UNIQUE,
    {ModsTable.LINK} TEXT NOT NULL,
    {ModsTable.TYPE} TEXT NOT NULL CHECK (type IN ('{TypeValues.FEATURE}', '{TypeValues.LIBRARY}')),
    {ModsTable.ROLE} TEXT NOT NULL CHECK (role IN ('{RoleValues.BOTH}', '{RoleValues.SERVER}', '{RoleValues.CLIENT}'))
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


TEMP_CHECK_TABLE = f'''
CREATE TEMP TABLE {ClientMods.TABLE_NAME} (
    {ClientMods.FILENAME} TEXT PRIMARY KEY,
    {ClientMods.FILEHASH} TEXT NOT NULL UNIQUE
) STRICT;
'''


#################################################################
# SQL for inserting values

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


INSERT_DEPENDENCY = f'''
INSERT INTO {DepsTable.TABLE_NAME} 
({DepsTable.MOD_ID},
{DepsTable.DEP_ID})
VALUES (?, ?);
'''


INSERT_CLIENT_MODS = f'''
INSERT INTO {ClientMods.TABLE_NAME}
({ClientMods.FILENAME},
{ClientMods.FILEHASH})
VALUES (?, ?);
'''


#################################################################
# SQL for selecting values

SELECT_ALL_MODS = f'''
SELECT * 
FROM {ModsTable.TABLE_NAME};
'''


SELECT_ONE_MOD = f'''
SELECT * 
FROM {ModsTable.TABLE_NAME} 
WHERE {ModsTable.ID} = ?;
'''


SELECT_MOD_DEPENDENCIES = f'''
SELECT {ModsTable.NAME}
FROM {DepsTable.TABLE_NAME}
JOIN {ModsTable.TABLE_NAME} on {ModsTable.TABLE_NAME}.{ModsTable.ID} = {DepsTable.DEP_ID}
WHERE {DepsTable.MOD_ID} = ?;
'''


SELECT_CLIENT_DOWNLOADS = f'''
SELECT {ModsTable.TABLE_NAME}.{ModsTable.FILENAME}
FROM {ModsTable.TABLE_NAME}
LEFT JOIN {ClientMods.TABLE_NAME} on {ClientMods.TABLE_NAME}.{ClientMods.FILENAME} = {ModsTable.TABLE_NAME}.{ModsTable.FILENAME}
WHERE {ModsTable.TABLE_NAME}.{ModsTable.ROLE} IN ('{RoleValues.BOTH}', '{RoleValues.CLIENT}')
AND ({ClientMods.TABLE_NAME}.{ClientMods.FILENAME} IS NULL 
OR {ClientMods.TABLE_NAME}.{ClientMods.FILEHASH} <> {ModsTable.TABLE_NAME}.{ModsTable.FILEHASH});
'''


SELECT_CLIENT_DELETES = f'''
SELECT {ClientMods.TABLE_NAME}.{ClientMods.FILENAME}
FROM {ClientMods.TABLE_NAME}
LEFT JOIN {ModsTable.TABLE_NAME} on {ModsTable.TABLE_NAME}.{ModsTable.FILENAME} = {ClientMods.TABLE_NAME}.{ClientMods.FILENAME}
WHERE {ModsTable.TABLE_NAME}.{ModsTable.FILENAME} IS NULL
OR {ModsTable.TABLE_NAME}.{ModsTable.ROLE} = '{RoleValues.SERVER}'
OR {ModsTable.TABLE_NAME}.{ModsTable.FILEHASH} <> {ClientMods.TABLE_NAME}.{ClientMods.FILEHASH};
'''


SELECT_CLIENT_CURRENT = f'''
SELECT {ModsTable.TABLE_NAME}.{ModsTable.FILENAME}
FROM {ModsTable.TABLE_NAME}
JOIN {ClientMods.TABLE_NAME} ON {ClientMods.TABLE_NAME}.{ClientMods.FILENAME} = {ModsTable.TABLE_NAME}.{ModsTable.FILENAME}
WHERE {ModsTable.TABLE_NAME}.{ModsTable.ROLE} IN ('{RoleValues.BOTH}', '{RoleValues.CLIENT}')
AND {ClientMods.TABLE_NAME}.{ClientMods.FILEHASH} = {ModsTable.TABLE_NAME}.{ModsTable.FILEHASH};
'''


SELECT_MOD_ROLE = f'''
SELECT {ModsTable.ROLE} 
FROM {ModsTable.TABLE_NAME} 
WHERE {ModsTable.FILENAME} = ?;'''


#################################################################
# SQL for updating mods

UPDATE_MOD = f'''
UPDATE {ModsTable.TABLE_NAME}
SET
    {ModsTable.NAME} = ?,
    {ModsTable.DESCRIPTION} = ?,
    {ModsTable.VERSION} = ?,
    {ModsTable.FILENAME} = ?,
    {ModsTable.FILEHASH} = ?,
    {ModsTable.LINK} = ?,
    {ModsTable.TYPE} = ?,
    {ModsTable.ROLE} = ?
WHERE {ModsTable.ID} = ?;
'''


#################################################################
# SQL for deleting mods

DELETE_MOD = f'''
DELETE 
FROM {ModsTable.TABLE_NAME} 
WHERE {ModsTable.ID} = ?;
'''