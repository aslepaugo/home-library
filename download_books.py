import os
import requests

from bs4 import BeautifulSoup
from pathlib import Path
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit


def check_for_redirect(response):
    if response.history and 300 < response.history[0].status_code < 400:
        raise requests.exceptions.HTTPError(f'Redirect from {response.history[0].url} ({response.history[0].status_code}, {response.url})')


def parse_book_data(url):
    response = requests.get(url)
    response.raise_for_status()
    try:
        check_for_redirect(response)
    except requests.exceptions.HTTPError:
        return None
    soup = BeautifulSoup(response.text, 'lxml')
    title, author = soup.find('div', {'id':'content'}).find('h1').text.split('::')
    image_url = soup.find('div', {'id':'content'}).find('img')['src']
    return {
        'title': title.strip(),
        'author': author.strip(),
        'image_url': urljoin('https://tululu.org', image_url),
        }


def download_txt(url, filename, folder='books'):
    outpath = Path.cwd() / folder
    Path.mkdir(outpath, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    try:
        check_for_redirect(response)
    except requests.exceptions.HTTPError:
        return None
    filepath = outpath / sanitize_filename(filename + '.txt')
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def download_image(url, folder='images'):
    outpath = Path.cwd() / folder
    Path.mkdir(outpath, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    try:
        check_for_redirect(response)
    except requests.exceptions.HTTPError:
        return None
    filename = urlsplit(url).path.split('/')[-1]

    filepath = outpath / sanitize_filename(filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


if __name__ == '__main__':
    for i in range(1, 11):
        book = parse_book_data(f'https://tululu.org/b{i}/')
        print(book)
        if book == None:
            continue
        download_txt(f'https://tululu.org/txt.php?id={i}', f"{i}. {book['title']}", 'books')
        download_image(book['image_url'])
