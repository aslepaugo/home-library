import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin


base_url = "https://tululu.org"
scince_fiction_url = "https://tululu.org/l55/"
response = requests.get(scince_fiction_url)
response.raise_for_status()
content = response.text
soup = BeautifulSoup(content, 'lxml')
book_link = soup.find('div', {'id':'content'}).find('table').find('a')['href']
url = urljoin(base_url, book_link)
print(url)
