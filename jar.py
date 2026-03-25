from zipfile import ZipFile
from tomlkit import loads, dumps, TOMLDocument


NEOFORGE_TOML_ZIP_PATH = 'META-INF/neoforge.mods.toml'


def get_toml_doc(zip: ZipFile) -> TOMLDocument|None:
    with zip.open(NEOFORGE_TOML_ZIP_PATH, 'r') as tomlFile:
        tomlBytes = tomlFile.read()

    return loads(tomlBytes.decode())


def get_metadata(jarPath: str):
    with ZipFile(jarPath, 'r') as zFile:
        tomlDoc = get_toml_doc(zFile)

    return tomlDoc


def get_dependancies():
    pass




