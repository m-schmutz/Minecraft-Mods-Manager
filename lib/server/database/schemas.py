#################################################################
# Python Lib Imports 

from enum import StrEnum


#################################################################
# Mods table schemas

class ModsTable(StrEnum):
    '''\'Mods\' Table Information'''
    TABLE_NAME = 'Mods'
    ID = 'id'
    NAME = 'name'
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


#################################################################
# Dependencies table schema

class DepsTable(StrEnum):
    '''\'Dependencies\' Table Information'''
    TABLE_NAME = 'Dependencies'
    MOD_ID = 'mod_id'
    DEP_ID = 'dep_id'


#################################################################
# Temporary check table schema

class ClientMods(StrEnum):
    '''Temp \'ClientMods\' Table Information'''
    TABLE_NAME = 'ClientMods'
    FILENAME = 'filename'
    FILEHASH = 'filehash'