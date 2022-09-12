from urllib.error import HTTPError
import requests

from pathlib import Path


def check_for_redirect(response):
    if response.history and 300 < response.history[0].status_code < 400:
        raise HTTPError(f'Redirect from {response.history[0].url} ({response.history[0].status_code}, {response.url})')


if __name__ == '__main__':
    outpath = Path.cwd() / 'books'
    Path.mkdir(outpath, exist_ok=True)
    for i in range(10):
        id = 3268 + i 
        url = f'https://tululu.org/txt.php?id={id}'
        response = requests.get(url)
        response.raise_for_status()
        try:
            check_for_redirect(response)
        except:
            continue
        filename = f'id{id}.txt'
        with open(outpath / filename, 'wb') as file:
            file.write(response.content)
