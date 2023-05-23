import requests
import config

from urllib.request import urlopen


def search(film):
    headers = {
        'accept': 'application/json',
        'X-API-KEY': config.KINOPOISK_TOKEN
    }

    response = requests.get(
        f'https://api.kinopoisk.dev/v1.2/movie/search?page=1&limit=10&query={film}',
        headers=headers)

    file = response.json()
    print(file)
    resource = urlopen(file['docs'][0]['poster'])
    out = open("img.jpg", 'wb')
    out.write(resource.read())
    out.close()

    return file['docs'][0]['name'], file['docs'][0]['description']
