PRAGMA foreign_keys = ON;

INSERT INTO category (categoryId, categoryName, categoryImage) VALUES
    (1, 'Classic Fiction',  'classic_fiction.jpg'),
    (2, 'Science Fiction',  'science_fiction.jpg'),
    (3, 'Mystery & Thriller', 'mystery_thriller.jpg'),
    (4, 'Nonfiction',       'nonfiction.jpg');

INSERT INTO book (categoryId, title, author, isbn, price, image, readNow) VALUES
    (1, 'To Kill a Mockingbird',  'Harper Lee',          '9780061120084', 18.99, 'to_kill_a_mockingbird.jpg', 1),
    (1, '1984',                   'George Orwell',       '9780451524935',  9.99, '1984.jpg',                  0),
    (1, 'The Great Gatsby',       'F. Scott Fitzgerald', '9780743273565', 15.00, 'the_great_gatsby.jpg',      1),
    (1, 'Pride and Prejudice',    'Jane Austen',         '9780141439518',  9.00, 'pride_and_prejudice.jpg',   0),
    (2, 'Dune',                                  'Frank Herbert',    '9780441172719', 10.99, 'dune.jpg',                  1),
    (2, 'The Hitchhiker''s Guide to the Galaxy', 'Douglas Adams',    '9780345391803',  8.99, 'hitchhikers_guide.jpg',     0),
    (2, 'Ender''s Game',                         'Orson Scott Card', '9780812550702',  8.99, 'enders_game.jpg',           0),
    (2, 'Project Hail Mary',                     'Andy Weir',        '9780593135204', 28.99, 'project_hail_mary.jpg',     1),
    (3, 'The Girl with the Dragon Tattoo', 'Stieg Larsson',      '9780307454546', 17.00, 'girl_with_the_dragon_tattoo.jpg', 0),
    (3, 'Gone Girl',                       'Gillian Flynn',      '9780307588371', 18.00, 'gone_girl.jpg',                   1),
    (3, 'And Then There Were None',        'Agatha Christie',    '9780062073488',  9.99, 'and_then_there_were_none.jpg',    1),
    (3, 'The Hound of the Baskervilles',   'Arthur Conan Doyle', '9780140437867',  8.00, 'hound_of_the_baskervilles.jpg',   0),
    (4, 'Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', '9780062316097', 24.99, 'sapiens.jpg',              1),
    (4, 'Educated',                              'Tara Westover',     '9780399590504', 28.00, 'educated.jpg',             0),
    (4, 'Atomic Habits',                         'James Clear',       '9780735211292', 27.00, 'atomic_habits.jpg',        1),
    (4, 'Thinking, Fast and Slow',               'Daniel Kahneman',   '9780374533557', 18.00, 'thinking_fast_and_slow.jpg', 0);
