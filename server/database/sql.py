from .schemas import ModsTable

# enforce foreign keys
FOREIGN_KEYS = 'PRAGMA foreign_keys = ON;'

# sql script to create tables if they do not exist
INIT_TABLES = f'''
CREATE TABLE IF NOT EXISTS {ModsTable.TABLE_NAME} (
    {ModsTable.ID} INTEGER PRIMARY KEY,
    {ModsTable.DISPLAY_NAME} TEXT NOT NULL UNIQUE,
    {ModsTable.DESCRIPTION} TEXT NOT NULL,
    {ModsTable.VERSION} TEXT NOT NULL,
    {ModsTable.FILENAME} TEXT NOT NULL UNIQUE,
    {ModsTable.FILEHASH} TEXT NOT NULL UNIQUE,
    {ModsTable.LINK} TEXT NOT NULL,
    {ModsTable.TYPE} TEXT NOT NULL CHECK (type IN ('Feature', 'Library')),
    {ModsTable.ROLE} TEXT NOT NULL CHECK (role IN ('Server', 'Client', 'Client/Server'))
) STRICT; 
'''
