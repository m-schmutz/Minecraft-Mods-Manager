#################################################################
# Python Lib Imports 

from zipfile import ZipFile, is_zipfile
from dataclasses import dataclass
from typing import Optional
from tomlkit import TOMLDocument, loads
from tomlkit.items import AoT, Table
from enum import StrEnum


#################################################################
# Enums

class TOMLDocKeys(StrEnum):
    MODSAOT = 'mods'
    DEPENDENCIES = 'dependencies'


class MetadataKeys(StrEnum):
    MODID = 'modId'
    VERSION = 'version'
    DISPLAYNAME = 'displayName'
    DISPLAYURL = 'displayURL'
    DESCRIPTION = 'description'
    SIDE = 'side'


#################################################################
# Constants

NEOFORGE_TOML_ZIP_PATH = 'META-INF/neoforge.mods.toml'


#################################################################
# Internal Functions

def _get_toml_doc(path: str) -> Optional[TOMLDocument]:
    try:
        with ZipFile(path, 'r') as zFile:

            with zFile.open(NEOFORGE_TOML_ZIP_PATH, 'r') as tFile:

                tBytes = tFile.read()

        return loads(tBytes.decode())

    except: 
        return None


def _get_metadata_table(doc: TOMLDocument) -> Table:
    modsAot: AoT = doc.get(TOMLDocKeys.MODSAOT)

    if type(modsAot) is not AoT:
        raise ValueError(f'Could not find \'{TOMLDocKeys.MODSAOT}\' AoT')
    
    if len(modsAot) != 1:
        raise ValueError(f'\'{TOMLDocKeys.MODSAOT}\' AoT should have length of 1')
    
    return modsAot[0]


def _get_dependency_list(doc: TOMLDocument, modId: str) -> AoT:
    depsTable: Table = doc.get(TOMLDocKeys.DEPENDENCIES)

    if type(depsTable) is not Table:
        raise ValueError(f'Could not find \'{TOMLDocKeys.DEPENDENCIES}\' table')
    
    depsAot: AoT = depsTable.get(modId)

    if type(depsAot) is not AoT:
        raise ValueError(f'Could not find \'{modId}\' dependency AoT')
    
    return depsAot


#################################################################
# JarFile Class

class JarFile:
    def __init__(self, path: str) -> None:
        if not is_zipfile(path):
            raise ValueError(f'{path} is not a valid jar file')
        
        self.path = path


    def metadata_tuple(self) -> tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]:
        tomlDoc = _get_toml_doc(self.path)

        if tomlDoc is None:
            raise ValueError('No neoforge toml file found in jar file')
        
        modTable = _get_metadata_table(tomlDoc)

        return (
            modTable.get(MetadataKeys.MODID),
            modTable.get(MetadataKeys.VERSION),
            modTable.get(MetadataKeys.DISPLAYNAME),
            modTable.get(MetadataKeys.DISPLAYURL),
            modTable.get(MetadataKeys.DESCRIPTION),
            modTable.get(MetadataKeys.SIDE)
        )
    

    def metadata_dict(self) -> dict[str, str]:
        tomlDoc = _get_toml_doc(self.path)

        if tomlDoc is None:
            raise ValueError('No neoforge toml file found in jar file')
        
        modTable = _get_metadata_table(tomlDoc)

        return {
            
        }

        



'''
get single table from mods aot
get dependency list
set table in mods aot
set dependency



'''