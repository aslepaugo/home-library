import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


BOOKS_ON_PAGE = 10
COLUMN_COUNT = 2

def on_reload():
    with open("books.json", "r", encoding='utf-8') as file:
        books = json.load(file)
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html"])
    )
    template = env.get_template("template.html")
    for page, books_chunk in enumerate(list(chunked(books, BOOKS_ON_PAGE))):
        rendered_page = template.render(
            books=list(chunked(books_chunk, COLUMN_COUNT))
        )
        with open(f"pages/index{page + 1}.html", "w", encoding="utf8") as file:
            file.write(rendered_page)    


if __name__ == "__main__":
    os.makedirs("pages", exist_ok=True)
    on_reload()
    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".")