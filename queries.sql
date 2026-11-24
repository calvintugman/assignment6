PRAGMA foreign_keys = ON;

-- Add a book
INSERT INTO book (categoryId, title, author, isbn, price, image, readNow)
VALUES (?, ?, ?, ?, ?, ?, ?);

-- All categories
SELECT categoryId, categoryName, categoryImage
FROM category
ORDER BY categoryId;

-- All books
SELECT bookId, title, author, isbn, price, readNow
FROM book
ORDER BY bookId;

-- Books in a category
SELECT b.bookId, b.title, b.author, b.price, c.categoryName
FROM book AS b
JOIN category AS c ON b.categoryId = c.categoryId
WHERE c.categoryId = ?
ORDER BY b.title;

-- Search by title
SELECT bookId, title, author, price
FROM book
WHERE title LIKE ?
ORDER BY title;

-- Update price
UPDATE book SET price = ? WHERE bookId = ?;

-- Delete a book
DELETE FROM book WHERE bookId = ?;

-- Search by author
SELECT bookId, title, author, price
FROM book
WHERE author LIKE ?
ORDER BY author, title;

-- Price range
SELECT bookId, title, author, price
FROM book
WHERE price BETWEEN ? AND ?
ORDER BY price;

-- Read Now books
SELECT b.bookId, b.title, b.author, c.categoryName
FROM book AS b
JOIN category AS c ON b.categoryId = c.categoryId
WHERE b.readNow = 1
ORDER BY b.title;

-- Count books per category
SELECT c.categoryId, c.categoryName, COUNT(b.bookId) AS bookCount
FROM category AS c
LEFT JOIN book AS b ON b.categoryId = c.categoryId
GROUP BY c.categoryId, c.categoryName
ORDER BY c.categoryId;
