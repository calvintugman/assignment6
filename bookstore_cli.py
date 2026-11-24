import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bookstore.db")


def get_connection():
    if not os.path.exists(DB_PATH):
        raise SystemExit(
            f"Database not found at {DB_PATH}.\n"
            "Create it first:\n"
            "  sqlite3 bookstore.db < createTables.sql\n"
            "  sqlite3 bookstore.db < insertRows.sql"
        )
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def print_table(rows, columns):
    if not rows:
        print("  No results found.")
        return

    def fmt(key, value):
        if key == "price":
            return f"${value:.2f}"
        if key == "readNow":
            return "Yes" if value else "No"
        return str(value)

    table = [[fmt(key, row[key]) for key, _ in columns] for row in rows]
    widths = [
        max(len(header), *(len(line[i]) for line in table))
        for i, (_, header) in enumerate(columns)
    ]

    header_line = "  ".join(h.ljust(w) for (_, h), w in zip(columns, widths))
    print("  " + header_line)
    for line in table:
        print("  " + "  ".join(cell.ljust(w) for cell, w in zip(line, widths)))


def prompt_int(message):
    while True:
        value = input(message).strip()
        try:
            return int(value)
        except ValueError:
            print("  Please enter a whole number.")


def prompt_price(message):
    while True:
        value = input(message).strip().lstrip("$")
        try:
            price = float(value)
        except ValueError:
            print("  Please enter a number, e.g. 12.99.")
            continue
        if price < 0:
            print("  Price cannot be negative.")
            continue
        return round(price, 2)


def prompt_text(message):
    while True:
        value = input(message).strip()
        if value:
            return value
        print("  This field cannot be empty.")


def prompt_yes_no(message):
    while True:
        value = input(message).strip().lower()
        if value in ("y", "yes"):
            return True
        if value in ("n", "no"):
            return False
        print("  Please enter y or n.")


BOOK_COLUMNS = [
    ("bookId", "ID"),
    ("title", "Title"),
    ("author", "Author"),
    ("price", "Price"),
]


def view_categories(conn):
    rows = conn.execute(
        "SELECT categoryId, categoryName, categoryImage "
        "FROM category ORDER BY categoryId"
    ).fetchall()
    print_table(rows, [
        ("categoryId", "ID"),
        ("categoryName", "Category"),
        ("categoryImage", "Image"),
    ])


def view_all_books(conn):
    rows = conn.execute(
        "SELECT b.bookId, b.title, b.author, b.isbn, b.price, b.readNow, "
        "       c.categoryName "
        "FROM book AS b "
        "JOIN category AS c ON b.categoryId = c.categoryId "
        "ORDER BY b.bookId"
    ).fetchall()
    print_table(rows, [
        ("bookId", "ID"),
        ("title", "Title"),
        ("author", "Author"),
        ("categoryName", "Category"),
        ("isbn", "ISBN"),
        ("price", "Price"),
        ("readNow", "Read Now"),
    ])


def view_books_in_category(conn):
    view_categories(conn)
    category_id = prompt_int("\nEnter category ID: ")

    rows = conn.execute(
        "SELECT b.bookId, b.title, b.author, b.price, c.categoryName "
        "FROM book AS b "
        "JOIN category AS c ON b.categoryId = c.categoryId "
        "WHERE c.categoryId = ? "
        "ORDER BY b.title",
        (category_id,),
    ).fetchall()

    if rows:
        print(f"\nBooks in '{rows[0]['categoryName']}':")
    print_table(rows, BOOK_COLUMNS)


def search_by_title(conn):
    keyword = prompt_text("Enter a title keyword: ")
    rows = conn.execute(
        "SELECT bookId, title, author, price FROM book "
        "WHERE title LIKE ? ORDER BY title",
        (f"%{keyword}%",),
    ).fetchall()
    print_table(rows, BOOK_COLUMNS)


def add_book(conn):
    view_categories(conn)
    category_id = prompt_int("\nCategory ID: ")
    exists = conn.execute(
        "SELECT 1 FROM category WHERE categoryId = ?", (category_id,)
    ).fetchone()
    if not exists:
        print("  No category with that ID. Book not added.")
        return

    title = prompt_text("Title: ")
    author = prompt_text("Author: ")
    isbn = prompt_text("ISBN: ")
    price = prompt_price("Price: ")
    image = prompt_text("Image filename (e.g. cover.jpg): ")
    read_now = 1 if prompt_yes_no("Feature as 'Read Now'? (y/n): ") else 0

    try:
        cursor = conn.execute(
            "INSERT INTO book (categoryId, title, author, isbn, price, image, readNow) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (category_id, title, author, isbn, price, image, read_now),
        )
        conn.commit()
    except sqlite3.IntegrityError as err:
        conn.rollback()
        print(f"  Could not add book: {err}")
        return
    print(f"  Added '{title}' with book ID {cursor.lastrowid}.")


def update_price(conn):
    book_id = prompt_int("Enter book ID: ")
    book = conn.execute(
        "SELECT title, price FROM book WHERE bookId = ?", (book_id,)
    ).fetchone()
    if not book:
        print("  No book with that ID.")
        return

    print(f"  '{book['title']}' currently costs ${book['price']:.2f}.")
    new_price = prompt_price("New price: ")
    conn.execute(
        "UPDATE book SET price = ? WHERE bookId = ?", (new_price, book_id)
    )
    conn.commit()
    print(f"  Price updated to ${new_price:.2f}.")


def delete_book(conn):
    book_id = prompt_int("Enter book ID to delete: ")
    book = conn.execute(
        "SELECT title FROM book WHERE bookId = ?", (book_id,)
    ).fetchone()
    if not book:
        print("  No book with that ID.")
        return

    if not prompt_yes_no(f"  Delete '{book['title']}'? (y/n): "):
        print("  Delete cancelled.")
        return
    conn.execute("DELETE FROM book WHERE bookId = ?", (book_id,))
    conn.commit()
    print("  Book deleted.")


def search_by_author(conn):
    keyword = prompt_text("Enter an author keyword: ")
    rows = conn.execute(
        "SELECT bookId, title, author, price FROM book "
        "WHERE author LIKE ? ORDER BY author, title",
        (f"%{keyword}%",),
    ).fetchall()
    print_table(rows, BOOK_COLUMNS)


def books_in_price_range(conn):
    low = prompt_price("Minimum price: ")
    high = prompt_price("Maximum price: ")
    if low > high:
        low, high = high, low
    rows = conn.execute(
        "SELECT bookId, title, author, price FROM book "
        "WHERE price BETWEEN ? AND ? ORDER BY price",
        (low, high),
    ).fetchall()
    print_table(rows, BOOK_COLUMNS)


def read_now_books(conn):
    rows = conn.execute(
        "SELECT b.bookId, b.title, b.author, c.categoryName "
        "FROM book AS b "
        "JOIN category AS c ON b.categoryId = c.categoryId "
        "WHERE b.readNow = 1 "
        "ORDER BY b.title"
    ).fetchall()
    print_table(rows, [
        ("bookId", "ID"),
        ("title", "Title"),
        ("author", "Author"),
        ("categoryName", "Category"),
    ])


def count_per_category(conn):
    rows = conn.execute(
        "SELECT c.categoryId, c.categoryName, COUNT(b.bookId) AS bookCount "
        "FROM category AS c "
        "LEFT JOIN book AS b ON b.categoryId = c.categoryId "
        "GROUP BY c.categoryId, c.categoryName "
        "ORDER BY c.categoryId"
    ).fetchall()
    print_table(rows, [
        ("categoryId", "ID"),
        ("categoryName", "Category"),
        ("bookCount", "Books"),
    ])


MENU = {
    "1": ("View all categories", view_categories),
    "2": ("View all books", view_all_books),
    "3": ("View books in a category", view_books_in_category),
    "4": ("Search books by title", search_by_title),
    "5": ("Add a new book", add_book),
    "6": ("Update a book price", update_price),
    "7": ("Delete a book", delete_book),
    "8": ("Quit", None),
    "9": ("Search books by author", search_by_author),
    "10": ("Show books within a price range", books_in_price_range),
    "11": ("Show 'Read Now' books", read_now_books),
    "12": ("Count books per category", count_per_category),
}


def print_menu():
    print("\nPage Turner Books")
    for key, (label, _) in MENU.items():
        print(f"  {key:>2}. {label}")


def main():
    conn = get_connection()
    try:
        while True:
            print_menu()
            choice = input("Choose an option: ").strip()
            if choice not in MENU:
                print("  Invalid choice, please try again.")
                continue

            label, action = MENU[choice]
            if action is None:
                print("Goodbye!")
                break
            print(f"\n{label}")
            action(conn)
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
