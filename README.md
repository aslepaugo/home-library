# Offline library from tululu.org

Script for downloading content from tululu.org (free library).

Helps to be prepared for free time without internet.

## How to prepare environment

I assume that python 3 is already installed. If not - you can download and install appropriate version from the offical [site](https://python.org).

1. Create virtual environment.

```bash
python -m venv venv
```

Activate your virtual environment:

```bash
. ./venv/bin/activate
# for Windows
# . ./venv/Scripts/activate
```

2. Install dependencies from requirements.txt.

```bash
pip install -r requirements.txt
```

3. You are ready to go with script.

## Script usage

### download_books

Script helps in books downloading from [tululu.org](tululu.org).

To download first 10 books.

```bash
python download_books.py
```

To download another specified set we should define paraneters `--start_id` and `end_id`

```bash
python download_books.py --start_id 930 --end_id 980
```

### parse_tululu_category

Script to download books from predefined category (SciFi by default).

There are following parameters:

`start_page` - Identify from which page you would like to start.
`end_page` - Identify on which page you would like to end (end page won't be parsed).
`dest_folder` - Folder to save books (default: books).
`json_path` - Path to json-file with book descriptions (default: books.json).
`skip_imgs` - Do not download images.
`skip_txt` - Do not download books.

Examples of usage:

1. Download all books from page 10 till the end without images, using default folders:

```bash
python parse_tululu_category.py --start_page 10 --skip_imgs
```

2. Define folders to store books and JSON file:

```bash
python parse_tululu_category.py --json_path "/home/user_name/my_books.json" --dest_folder "/home/user_name/books_folder"
```
