from requests import get




modFilename = 'travelersbackpack-neoforge-1.21.1-10.1.32.jar'

downloadUrl = f'http://localhost:5000/api/download/mod/{modFilename}'


if __name__ == '__main__':
    with get(downloadUrl, stream=True) as r:
        r.raise_for_status()

        with open(modFilename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
