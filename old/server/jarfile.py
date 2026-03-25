#################################################################
# Python Lib Imports 

from zipfile import ZipFile, is_zipfile
from dataclasses import dataclass
from typing import Optional
from tomlkit import TOMLDocument, loads


NEOFORGE_TOML_ZIP_PATH = 'META-INF/neoforge.mods.toml'

#################################################################
# Util Functions

def _get_toml_doc(path: str) -> Optional[TOMLDocument]:
    try:
        with ZipFile(path, 'r') as zFile:

            with zFile.open(NEOFORGE_TOML_ZIP_PATH, 'r') as tFile:

                tBytes = tFile.read()

        return loads(tBytes.decode())

    except: 
        return None


#################################################################


@dataclass
class Metadata:
    modId: Optional[str]
    version: Optional[str]
    displayName: Optional[str]
    displayURL: Optional[str]
    description: Optional[str]
    side = Optional[str]

    def __init__(self, metaDict: dict[str, str]):
        self.modId = metaDict.get('modId')
        self.version = metaDict.get('version')
        self.displayName = metaDict.get('displayName')
        self.displayURL = metaDict.get('displayURL')
        self.description = metaDict.get('description')
        self.side = metaDict.get('side')
                    





#################################################################
# JarFile Class

class JarFile:
    def __init__(self, path: str) -> None:
        if not is_zipfile(path):
            raise ValueError(f'{path} is not a valid jar file')
        
        self.path = path


    def extract_metadata(self) -> Metadata:
        tomlDoc = _get_toml_doc(self.path)

        if tomlDoc is None:
            raise ValueError('No neoforge toml file found in jar file')
        
        modsAot: Optional[list[dict[str, str]]] = tomlDoc.get('mods')

        if modsAot is None:
            raise ValueError('No mods array of tables was found')
        
        if len(modsAot) != 1:
            raise ValueError('Expected only one element in mods array of tables')
        
        if modsAot[0] is not dict:
            raise ValueError('Unexpected type in mods array of tables')

        return Metadata(modsAot[0])






