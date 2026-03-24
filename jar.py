#!./venv-server/bin/python3

from zipfile import ZipFile
from tomlkit import loads, dumps


jarPath = '/home/msch/Projects/Minecraft-Mods-Manager/examples/sample_files/alexsmobs-1.22.16.jar'

tomlPath = '/home/msch/Projects/Minecraft-Mods-Manager/examples/sample_files/neoforge.mods.toml'




def get_metadata(jarPath: str) -> tuple|None:
    pass
















with open(tomlPath, 'r') as f:
    tomlStr = f.read()



doc = loads(tomlStr)


print(doc)
