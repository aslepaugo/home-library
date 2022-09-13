from urllib.error import HTTPError
import requests

from pathlib import Path
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history and 300 < response.history[0].status_code < 400:
        raise HTTPError(f'Redirect from {response.history[0].url} ({response.history[0].status_code}, {response.url})')


def download_txt(url, filename, folder='books'):
    outpath = Path.cwd() / 'books'
    Path.mkdir(outpath, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    try:
        check_for_redirect(response)
    except HTTPError:
        return None
    filepath = outpath / sanitize_filename(filename + '.txt')
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


if __name__ == '__main__':
    pass
