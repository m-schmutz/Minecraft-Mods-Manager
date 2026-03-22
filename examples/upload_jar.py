from requests import post
from sys import argv
from os.path import dirname, abspath, join


def get_examples_dir():
    scriptPath = argv[0]

    examplesDir = dirname(scriptPath)

    return abspath(examplesDir)


if __name__ == '__main__':
    examplesDir = get_examples_dir()

    modFilePath = join(examplesDir, 'sample_files', 'alexsmobs-1.22.16.jar')

    # metadata needed with a mod upload
    metaData = {
        'name': 'Alex\'s Mobs (Unofficial Port)', 
        'description': '85+ New mobs with stylistic quality above the default game.', 
        'version': '1.22.16',
        'link': 'https://www.curseforge.com/minecraft/mc-mods/alexs-mobs-1-21-1-port',
        'type': 'Feature',
        'role': 'Client/Server'
    }

    with open(modFilePath, 'rb') as fp:

        resp = post('http://localhost:5000/api/admin/upload/mod', files={'mod-file': fp}, data=metaData)
        print(resp.json())