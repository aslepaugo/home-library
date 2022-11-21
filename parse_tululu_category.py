import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin


base_url = "https://tululu.org"
scince_fiction_url = "https://tululu.org/l55"
max_page = 10

for page in range(1, max_page + 1):
    response = requests.get(f"{scince_fiction_url}/{page}")
    response.raise_for_status()
    content = response.text
    soup = BeautifulSoup(content, 'lxml')
    book_cards = soup.find('div', {'id':'content'}).find_all('table')
    for book_card in book_cards:
        book_link = book_card.find('a')['href']
        url = urljoin(base_url, book_link)
        print(url)
