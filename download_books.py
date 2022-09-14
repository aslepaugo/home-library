import argparse
import requests
import sys
import time

from bs4 import BeautifulSoup
from pathlib import Path
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit


def check_for_redirect(response):
    if response.history and 300:
        raise requests.exceptions.HTTPError(f'Redirect from {response.history[0].url} ({response.history[0].status_code}, {response.url})')


def parse_book_page(content):
    soup = BeautifulSoup(content, 'lxml')
    title, author = soup.find('div', {'id':'content'}).find('h1').text.split('::')
    image_path = soup.find('div', {'id':'content'}).find('img')['src']
    comment_blocks = soup.find('div', {'id':'content'}).find_all(class_='texts')
    comments = [comment_block.find('span').text for comment_block in comment_blocks]
    genre_block = soup.find('span', class_='d_book').find_all('a')
    genres = [genre.text for genre in genre_block]
    return {
        'title': title.strip(),
        'author': author.strip(),
        'image_path': image_path,
        'comments': comments,
        'genres': genres,
        }


def download_txt(url, filename, folder='books'):
    outpath = Path.cwd() / folder
    Path.mkdir(outpath, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    filepath = outpath / sanitize_filename(filename + '.txt')
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def download_image(url, folder='images'):
    outpath = Path.cwd() / folder
    Path.mkdir(outpath, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    filename = urlsplit(url).path.split('/')[-1]
    filepath = outpath / sanitize_filename(filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script for downloading books from https://tululu.org')
    parser.add_argument('--start_id', help='Start ID for book', type=int, default=1)
    parser.add_argument('--end_id', help='End ID for book', type=int, default=10)
    args = parser.parse_args()
    for book_id in range(args.start_id, args.end_id + 1):     
        try:
            book_url = f'https://tululu.org/b{book_id}/'
            response = requests.get(book_url)
            response.raise_for_status()
            check_for_redirect(response)
            book = parse_book_page(response.text)
            download_txt(f'https://tululu.org/txt.php?id={book_id}', f"{book_id}. {book['title']}", 'books')
            download_image(urljoin(book_url, book['image_path']), 'images')
        except requests.exceptions.HTTPError as err:
            print(err, file=sys.stderr)
            continue        
        except requests.exceptions.ConnectionError as err:
            print(err, file=sys.stderr)
            time.sleep(5)
