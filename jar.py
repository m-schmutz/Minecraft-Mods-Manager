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


def extract_metadata(doc: TOMLDocument) -> tuple:
    modsAot = doc.get('mods')

    if (len(modsAot) != 1):
        raise RuntimeError('Expected only one mod in array of tables')
    
    return (
        modsAot[0]['modId'],
        modsAot[0]['version'],
        modsAot[0]['displayName'],
        modsAot[0]['displayURL'],
        modsAot[0]['description'],
    )


def extract_dependancies(doc: TOMLDocument) -> tuple:
    pass




