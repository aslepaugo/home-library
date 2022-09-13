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

To download first 10 books.

```bash
python download_books.py
```

To download another specified set we should define paraneters `--start_id` and `end_id`

```bash
python download_books.py --start_id 930 --end_id 980
```

