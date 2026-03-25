#################################################################
# Python Lib Imports 

from zipfile import ZipFile, is_zipfile
from dataclasses import dataclass
from typing import Optional
from tomlkit import TOMLDocument, loads
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


def _extract_mods_aot(doc: TOMLDocument):
    aot = doc.get(TOMLDocKeys.MODSAOT)

