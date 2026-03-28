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


class DependencyKeys(StrEnum):
    MODID = 'modId'
    MANDATORY = 'mandatory'
    VERSIONRANGE = 'versionRange'
    SIDE = 'side'


#################################################################
# Constants

NEOFORGE_TOML_ZIP_PATH = 'META-INF/neoforge.mods.toml'


#################################################################
# Internal Functions

def _update_jar(jarPath: str, doc: TOMLDocument):
    pass


def _new_toml_doc():
    pass


def _get_toml_doc(jarPath: str):
    try:
        with ZipFile(jarPath, 'r') as zFile:

            with zFile.open(NEOFORGE_TOML_ZIP_PATH, 'r') as tFile:

                tBytes = tFile.read()

        return loads(tBytes.decode())

    except: 
        return _new_toml_doc()
    

def _extract_metadata_table(doc: TOMLDocument) -> Table:
    modsAot: AoT = doc.get(TOMLDocKeys.MODSAOT)

    if type(modsAot) is not AoT:
        raise ValueError(f'Could not find \'{TOMLDocKeys.MODSAOT}\' AoT')
    
    if len(modsAot) != 1:
        raise ValueError(f'\'{TOMLDocKeys.MODSAOT}\' AoT should have length of 1')
    
    return modsAot[0]


def _extract_dependency_aot(doc: TOMLDocument, modId: str):
    pass


#################################################################
# JarFile Class

class JarFile:
    def __init__(self, path: str) -> None:
        if not is_zipfile(path):
            raise ValueError(f'{path} is not a valid jar file')
        
        self.path = path


    def get_toml_data(self) -> dict:
        tomlDoc = _get_toml_doc(self.path)

        metadataTable = _extract_metadata_table(tomlDoc)

        return {str(k): metadataTable.get(k) for k in MetadataKeys}







