import argparse
import json
import re
import requests
import sys
import time

from bs4 import BeautifulSoup
from urllib.parse import urljoin

import download_books


def create_parser():
    parser = argparse.ArgumentParser(
        description = "Script to download books from https://tululu.org by predefined category (SciFi by default)."
    )
    parser.add_argument("--start_page", type=int, default=1,
                        help="Identify from which page you would like to start.")
    parser.add_argument("--end_page", type=int,
                        help="Identify on which page you would like to end (end page won't be parsed).")
    parser.add_argument("--dest_folder", type=str, default="books",
                        help="Folder to save books (default: books).")
    parser.add_argument("--skip_imgs", action="store_true",
                        help="Do not download images.")
    parser.add_argument("--skip_txt", action="store_true",
                        help="Do not download books.")
    parser.add_argument("--json_path", type=str, default="books.json",
                        help="Path to json-file with book descriptions (default: books.json).")
    return parser


def get_end_page(url, end_page=None):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    max_page = int(soup.select_one("p.center > :last-child").text)
    if not end_page or end_page <= start_page or end_page > max_page + 1:
        end_page = max_page + 1
    return end_page


def get_book_links(url, start_page, end_page):
    book_links = []
    for page in range(start_page, end_page):
        try:
            response = requests.get(f"{url}/{page}")
            response.raise_for_status()
            download_books.check_for_redirect(response)
            content = response.text
            soup = BeautifulSoup(content, 'lxml')
            book_links += [book_link_tag['href'] for book_link_tag in soup.select('.bookimage a')]
        except requests.exceptions.HTTPError as err:
            print(err, file=sys.stderr)
            continue        
        except requests.exceptions.ConnectionError as err:
            print(err, file=sys.stderr)
            time.sleep(5)
            continue       
    return book_links


if __name__ == '__main__':
    base_url = "https://tululu.org"
    scince_fiction_url = "https://tululu.org/l55"
    parser = create_parser()
    args = parser.parse_args()
    start_page = args.start_page
    end_page = get_end_page(url=scince_fiction_url, end_page=args.end_page)
    book_links = get_book_links(url=scince_fiction_url, start_page=start_page, end_page=end_page)
    books = []
    for book_link in book_links:
        book_url = urljoin(base_url, book_link)
        book_id = re.findall(r'\d+', book_link)[0]
        try:
            response = requests.get(book_url)
            response.raise_for_status()
            download_books.check_for_redirect(response)
            book = download_books.parse_book_page(response.text)
            if not book['txt_link']:
                print(f'There is no TXT book for the link {book_url}')
                continue
            books.append(book)
            if not args.skip_txt:
                download_books.download_txt(
                    'https://tululu.org/txt.php', 
                    book_id, 
                    f"{book_id}. {book['title']}", 
                    args.dest_folder
                )
            if not args.skip_imgs:
                download_books.download_image(urljoin(book_url, book['image_path']), 'images')
        except requests.exceptions.HTTPError as err:
            print(err, file=sys.stderr)
            continue        
        except requests.exceptions.ConnectionError as err:
            print(err, file=sys.stderr)
            time.sleep(5)
            continue

    with open(args.json_path, "w", encoding="utf8") as file:
        json.dump(books, file, ensure_ascii=False)
