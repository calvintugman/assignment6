# Page Turner Books

**Name:** Calvin Tugman

## Description

Page Turner Books is a small bookstore that sells classic fiction, science fiction, mystery, and nonfiction. This project stores the books in a SQLite database and lets you manage them with a Python command-line program.

## Create the database

```sh
sqlite3 bookstore.db < createTables.sql
sqlite3 bookstore.db < insertRows.sql
```

## Run the program

```sh
python3 bookstore_cli.py
```

## Extra features

- Search books by author
- Show books in a price range
- Show "Read Now" books
- Count books per category
