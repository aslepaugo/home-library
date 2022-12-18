import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def on_reload():
    with open("books.json", "r", encoding='utf-8') as file:
        books_data = file.read()
    books = json.loads(books_data)
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html"])
    )
    template = env.get_template("template.html")
    rendered_page = template.render(
        books=books,
    )
    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)    


if __name__ == "__main__":
    on_reload()
    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".")
