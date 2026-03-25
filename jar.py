from zipfile import ZipFile
from tomlkit import loads, dumps, TOMLDocument
from typing import Optional


NEOFORGE_TOML_ZIP_PATH = 'META-INF/neoforge.mods.toml'


def get_toml_doc(jarPath: str) -> Optional[TOMLDocument]:

    try:
        with ZipFile(jarPath, 'r') as zFile:

            with zFile.open(NEOFORGE_TOML_ZIP_PATH, 'r') as tFile:

                tBytes = tFile.read()
        
        return loads(tBytes.decode())
    
    except:
        return None













def get_dependancies():
    pass




