from requests import post


# this should be a dictionary that maps filenames to their corresponding filehash's
clientModsInfo = {
    'travelersbackpack-neoforge-1.21.1-10.1.32.jar': '3a83b57b7bbeb720016e45eb37887c4cfc11d2deb1ec0425c56d5e0c75da824f'
}


if __name__ == '__main__':
    resp = post('http://localhost:5000/api/info/check-client', json=clientModsInfo)
    print(resp.json())

