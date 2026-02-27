from enum import StrEnum


############ Mods Table ############


class ModsTable(StrEnum):
    '''\'Mods\' Table Information'''
    TABLE_NAME = 'Mods'
    ID = 'id'
    DISPLAY_NAME = 'display_name'
    DESCRIPTION = 'description'
    VERSION = 'version'
    FILENAME = 'filename'
    FILEHASH = 'filehash'
    LINK = 'link'
    TYPE = 'type'
    ROLE = 'role'


class TypeValues(StrEnum):
    '''Allowed values for the MOD_TYPE column in the \'Mods\' table'''
    FEATURE = 'Feature'
    LIBRARY = 'Library'


class RoleValues(StrEnum):
    '''Allowed values for the MOD_ROLE column in the \'Mods\' table'''
    SERVER = 'Server'
    CLIENT = 'Client'
    BOTH = 'Client/Server'


############ Dependancies Table ############


class DepsTable(StrEnum):
    '''\'Dependancies\' Table Information'''
    TABLE_NAME = 'Dependancies'
    ID = 'id'
    MOD_ID = 'mod_id'
    DEP_ID = 'dep_id'

