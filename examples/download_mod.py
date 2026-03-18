from requests import get




modFilename = 'travelersbackpack-neoforge-1.21.1-10.1.32.jar'


if __name__ == '__main__':
    resp = get(f'http://localhost:5000/api/download/mod/{modFilename}', stream=True)
    

    print(f'{resp.headers["Content-Disposition"]}')
