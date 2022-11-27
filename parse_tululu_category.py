import json
import re
import requests
import sys
import time

from bs4 import BeautifulSoup
from urllib.parse import urljoin

import download_books


base_url = "https://tululu.org"
scince_fiction_url = "https://tululu.org/l55"
max_page = 2
books = []
for page in range(1, max_page + 1):
    response = requests.get(f"{scince_fiction_url}/{page}")
    response.raise_for_status()
    content = response.text
    soup = BeautifulSoup(content, 'lxml')
    book_cards = soup.find('div', {'id':'content'}).find_all('table')
    for book_card in book_cards:
        book_link = book_card.find('a')['href']
        book_url = urljoin(base_url, book_link)
        book_id = re.findall(r'\d+', book_link)[0]
        try:
            response = requests.get(book_url)
            response.raise_for_status()
            download_books.check_for_redirect(response)
            book = download_books.parse_book_page(response.text)
            if not book['txt_link']:
                raise requests.exceptions.HTTPError
            print(f"{book.get('txt_link')}")
            books.append(book)
            download_books.download_txt('https://tululu.org/txt.php', book_id, f"{book_id}. {book['title']}", 'books')
            download_books.download_image(urljoin(book_url, book['image_path']), 'images')
        except requests.exceptions.HTTPError as err:
            print(err, file=sys.stderr)
            continue        
        except requests.exceptions.ConnectionError as err:
            print(err, file=sys.stderr)
            time.sleep(5)
            continue


with open("books.json", "w", encoding="utf8") as file:
    json.dump(books, file, ensure_ascii=False)
