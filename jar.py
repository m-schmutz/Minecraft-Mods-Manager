#!./venv-server/bin/python3


from tomlkit import loads, dumps





jarPath = '/home/msch/Projects/Minecraft-Mods-Manager/examples/sample_files/alexsmobs-1.22.16.jar'

tomlPath = '/home/msch/Projects/Minecraft-Mods-Manager/examples/sample_files/neoforge.mods.toml'


with open(tomlPath, 'r') as f:
    tomlData = f.read()



doc = loads(tomlData)


print(doc)
