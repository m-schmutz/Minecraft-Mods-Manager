from requests import post
from sys import argv
from os.path import dirname, abspath, join


def get_examples_dir():
    scriptPath = argv[0]

    examplesDir = dirname(scriptPath)

    return abspath(examplesDir)


if __name__ == '__main__':
    examplesDir = get_examples_dir()

    zipFilePath = join(examplesDir, 'sample_files', 'upload_test.zip')

    manifestFilePath = join(examplesDir, 'sample_files', 'manifest.json')

    with open(zipFilePath, 'rb') as zFp, open(manifestFilePath, 'rb') as mFp:
        
        resp = post('http://localhost:5000/api/admin/upload/mods', files={'mods-zip': zFp, 'manifest': mFp})
        print(resp.json())