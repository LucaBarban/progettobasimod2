INSERT INTO genres (name) VALUES
    ('Action'),
    ('Adventure'),
    ('Classic'),
    ('Comedy'),
    ('Drama'),
    ('Fantasy'),
    ('Horror'),
    ('Literary Fiction'),
    ('Mystery'),
    ('Romance'),
    ('Sci-Fi'),
    ('Thriller');

INSERT INTO authors (first_name, last_name) VALUES
    ('Jane', 'Austen'),
    ('Charles', 'Dickens'),
    ('Ernest', 'Hemingway'),
    ('Virginia', 'Woolf'),
    ('F. Scott', 'Fitzgerald'),
    ('Leo', 'Tolstoy'),
    ('Emily', 'Brontë'),
    ('Mark', 'Twain'),
    ('J.K.', 'Rowling'),
    ('Harper', 'Lee'),
    ('Toni', 'Morrison'),
    ('Gabriel', 'García Márquez'),
    ('George', 'Orwell'),
    ('Agatha', 'Christie'),
    ('Stephen', 'King'),
    ('Chimamanda Ngozi', 'Adichie');

INSERT INTO publishers (name) VALUES
    ('Penguin Books'),
    ('HarperCollins'),
    ('Random House'),
    ('Simon & Schuster'),
    ('Macmillan Publishers'),
    ('Hachette Livre'),
    ('Oxford University Press'),
    ('Pearson Education');

INSERT INTO books (title, published, pages, isbn, fk_author, fk_publisher) VALUES
    ('Pride and Prejudice', '1813-01-28', 279, '9780141439518', 1, 'Penguin Books'),
    ('Great Expectations', '1861-01-01', 544, '9780141439563', 2, 'Penguin Books'),
    ('The Old Man and the Sea', '1952-09-01', 127, '9780684801223', 3, 'Simon & Schuster'),
    ('To the Lighthouse', '1927-05-05', 209, '9780156907392', 4, 'HarperCollins'),
    ('The Great Gatsby', '1925-04-10', 180, '9780743273565', 5, 'Random House'),
    ('Anna Karenina', '1878-03-28', 964, '9780143035008', 6, 'Penguin Books'),
    ('Wuthering Heights', '1847-12-19', 384, '9780141439556', 7, 'Penguin Books'),
    ('The Adventures of Huckleberry Finn', '1884-12-10', 366, '9780143107323', 8, 'Penguin Books'),
    ('Harry Potter and the Sorcerer''s Stone', '1997-06-26', 309, '9780747532743', 9, 'Random House'),
    ('To Kill a Mockingbird', '1960-07-11', 324, '9780060935467', 10, 'HarperCollins'),
    ('Beloved', '1987-09-02', 324, '9780140280494', 11, 'Random House'),
    ('One Hundred Years of Solitude', '1967-05-30', 417, '9780060883287', 12, 'HarperCollins'),
    ('1984', '1949-06-08', 328, '9780451524935', 13, 'Penguin Books'),
    ('Murder on the Orient Express', '1934-01-01', 274, '9780062693662', 14, 'HarperCollins'),
    ('The Shining', '1977-01-28', 447, '9780307743657', 15, 'Random House'),
    ('Half of a Yellow Sun', '2006-08-11', 433, '9781400044160', 16, 'Random House'),
    ('Emma', '1815-12-23', 474, '9780141439587', 1, 'Penguin Books'),
    ('David Copperfield', '1850-05-01', 882, '9780140439441', 2, 'Penguin Books'),
    ('One Flew Over the Cuckoo''s Nest', '1962-02-01', 320, '9780451163967', 8, 'Simon & Schuster'),
    ('The Catcher in the Rye', '1951-07-16', 234, '9780316769488', 8, 'Penguin Books'),
    ('The Picture of Dorian Gray', '1890-07-20', 254, '9780486278070', 5, 'Penguin Books'),
    ('Crime and Punishment', '1866-11-14', 430, '9780679734505', 6, 'Penguin Books'),
    ('Gone with the Wind', '1936-06-30', 1037, '9780446675536', 10, 'HarperCollins'),
    ('The Hobbit', '1937-09-21', 310, '9780345339683', 9, 'Random House'),
    ('Moby-Dick', '1851-10-18', 585, '9780142000083', 2, 'Penguin Books'),
    ('The Road', '2006-09-26', 287, '9780307387899', 15, 'Simon & Schuster'),
    ('Americanah', '2013-05-14', 588, '9780307455925', 16, 'HarperCollins'),
    ('Sense and Sensibility', '1811-10-30', 352, '9780141439662', 1, 'Penguin Books'),
    ('Les Misérables', '1862-03-15', 1232, '9780140444308', 6, 'Penguin Books'),

    ('The Sun Also Rises', '1926-10-22', 251, '9780684800714', 3, 'Simon & Schuster');
INSERT INTO booksgenres (fk_idB, fk_genre) VALUES
    (1, 'Romance'),
    (1, 'Classic'),
    (2, 'Classic'),
    (3, 'Adventure'),
    (3, 'Literary Fiction'),
    (4, 'Sci-Fi'),
    (5, 'Classic'),
    (5, 'Literary Fiction'),
    (6, 'Classic'),
    (6, 'Romance'),
    (7, 'Drama'),
    (8, 'Adventure'),
    (8, 'Classic'),
    (9, 'Fantasy'),
    (9, 'Comedy'),
    (10, 'Literary Fiction'),
    (10, 'Horror'),
    (11, 'Mystery'),
    (12, 'Literary Fiction'),
    (13, 'Sci-Fi'),
    (13, 'Thriller'),
    (14, 'Mystery'),
    (15, 'Horror'),
    (16, 'Classic'),
    (16, 'Adventure'),
    (17, 'Romance'),
    (17, 'Classic'),
    (18, 'Classic'),
    (19, 'Literary Fiction'),
    (20, 'Classic'),
    (21, 'Literary Fiction'),
    (22, 'Classic'),
    (23, 'Adventure'),
    (23, 'Fantasy'),
    (24, 'Adventure'),
    (25, 'Classic'),
    (26, 'Literary Fiction'),
    (27, 'Classic'),
    (28, 'Adventure'),
    (28, 'Romance'),
    (29, 'Adventure'),
    (29, 'Drama'),
    (30, 'Sci-Fi');

INSERT INTO users (username, first_name, last_name, password, created_at, balance, seller, last_logged_in_at, token) VALUES
    ('alice123', 'Alice', 'Johnson', '$2b$10$Oy7A3rGnu9X8BXZ40oazEeg72SXO3KBb8lAhjgjKwGL3Msk4BPE/q', '2023-01-15', 15000, true, NOW(), '{}'),
    ('bob_smith', 'Bob', 'Smith', '$2b$10$Oy7A3rGnu9X8BXZ40oazEeg72SXO3KBb8lAhjgjKwGL3Msk4BPE/q', '2023-02-20', 750, false, NOW(), '{}'),
    ('jane_doe', 'Jane', 'Doe', '$2b$10$Oy7A3rGnu9X8BXZ40oazEeg72SXO3KBb8lAhjgjKwGL3Msk4BPE/q', '2023-03-10', 300, false, NOW(), '{}'),
    ('mike87', 'Mike', 'Johnson', '$2b$10$Oy7A3rGnu9X8BXZ40oazEeg72SXO3KBb8lAhjgjKwGL3Msk4BPE/q', '2023-04-05', 1000, true, NOW(), '{}'),
    ('sara_miller', 'Sara', 'Miller', '$2b$10$Oy7A3rGnu9X8BXZ40oazEeg72SXO3KBb8lAhjgjKwGL3Msk4BPE/q', '2023-05-12', 200, false, NOW(), '{}'),
    ('max_king', 'Max', 'King', '$2b$10$Oy7A3rGnu9X8BXZ40oazEeg72SXO3KBb8lAhjgjKwGL3Msk4BPE/q', '2023-06-18', 800, true, NOW(), '{}'),
    ('emily_green', 'Emily', 'Green', '$2b$10$Oy7A3rGnu9X8BXZ40oazEeg72SXO3KBb8lAhjgjKwGL3Msk4BPE/q', '2023-07-22', 600, false, NOW(), '{}'),
    ('chris99', 'Chris', 'Johnson', '$2b$10$Oy7A3rGnu9X8BXZ40oazEeg72SXO3KBb8lAhjgjKwGL3Msk4BPE/q', '2023-08-30', 400, true, NOW(), '{}'),
    ('lisa_wang', 'Lisa', 'Wang', '$2b$10$Oy7A3rGnu9X8BXZ40oazEeg72SXO3KBb8lAhjgjKwGL3Msk4BPE/q', '2023-09-14', 900, false, NOW(), '{}'),
    ('alex23', 'Alex', 'Brown', '$2b$10$Oy7A3rGnu9X8BXZ40oazEeg72SXO3KBb8lAhjgjKwGL3Msk4BPE/q', '2023-10-25', 350, true, NOW(), '{}');


-- User: alice123
INSERT INTO owns (fk_username, fk_book, quantity, state, price) VALUES
    ('alice123', 1, 5, 'new', 2000),
    ('alice123', 2, 4, 'as new', -1),
    ('alice123', 3, 3, 'used', 1000),
    ('alice123', 4, 6, 'new', -1),
    ('alice123', 5, 7, 'as new', 1500),
    ('alice123', 6, 5, 'used', -1),
    ('alice123', 7, 4, 'new', 1750),
    ('alice123', 8, 3, 'as new', -1),
    ('alice123', 9, 2, 'used', 800),
    ('alice123', 10, 7, 'new', -1),
    ('alice123', 11, 6, 'as new', 700),
    ('alice123', 12, 5, 'used', -1),
    ('alice123', 13, 4, 'new', 2500),
    ('alice123', 14, 3, 'as new', -1),
    ('alice123', 15, 2, 'used', 1050);
-- User: bob_smith

INSERT INTO owns (fk_username, fk_book, quantity, state, price) VALUES
    ('bob_smith', 16, 5, 'new', -1),
    ('bob_smith', 17, 4, 'as new', -1),
    ('bob_smith', 18, 3, 'used', -1),
    ('bob_smith', 19, 6, 'new', -1),
    ('bob_smith', 20, 7, 'as new', -1);

-- User: jane_doe
INSERT INTO owns (fk_username, fk_book, quantity, state, price) VALUES
    ('jane_doe', 21, 5, 'used', -1),
    ('jane_doe', 22, 4, 'new', -1),
    ('jane_doe', 23, 3, 'as new', -1),
    ('jane_doe', 24, 6, 'used', -1),
    ('jane_doe', 25, 7, 'new', -1);

-- User: mike87
INSERT INTO owns (fk_username, fk_book, quantity, state, price) VALUES
    ('mike87', 26, 5, 'as new', -1),
    ('mike87', 27, 4, 'used', 1200),
    ('mike87', 28, 3, 'new', 3500),
    ('mike87', 29, 6, 'as new', 1599),
    ('mike87', 30, 7, 'used', 999);

-- Insert owned books for user 'sara_miller'
INSERT INTO owns (fk_username, fk_book, quantity, state, price) VALUES
    ('sara_miller', 1, 3, 'new', -1),
    ('sara_miller', 2, 4, 'as new', -1),
    ('sara_miller', 3, 2, 'used', -1);

-- Insert owned books for user 'max_king'
INSERT INTO owns (fk_username, fk_book, quantity, state, price) VALUES
    ('max_king', 4, 5, 'new', 2050),
    ('max_king', 5, 3, 'as new', 1499),
    ('max_king', 6, 4, 'used', -1),
    ('max_king', 7, 2, 'new', -1);

-- Insert owned books for user 'emily_green'
INSERT INTO owns (fk_username, fk_book, quantity, state, price) VALUES
    ('emily_green', 8, 4, 'as new', -1),
    ('emily_green', 9, 3, 'used', -1),
    ('emily_green', 10, 2, 'new', -1);

-- Insert owned books for user 'chris99'
INSERT INTO owns (fk_username, fk_book, quantity, state, price) VALUES
    ('chris99', 11, 3, 'as new', -1),
    ('chris99', 12, 4, 'used', -1),
    ('chris99', 13, 2, 'new', 1399),
    ('chris99', 14, 5, 'as new', 1200);

-- Insert owned books for user 'lisa_wang'
INSERT INTO owns (fk_username, fk_book, quantity, state, price) VALUES
    ('lisa_wang', 15, 4, 'used', -1),
    ('lisa_wang', 16, 3, 'new', -1),
    ('lisa_wang', 17, 2, 'as new', -1);

-- Insert owned books for user 'alex23'
INSERT INTO owns (fk_username, fk_book, quantity, state, price) VALUES
    ('alex23', 18, 3, 'used', 899),
    ('alex23', 19, 4, 'new', 1550),
    ('alex23', 20, 2, 'as new', 1399),
    ('alex23', 21, 5, 'used', -1),
    ('alex23', 22, 3, 'new', -1);

-- Add cart entries
-- Cart entry 1: Buyer 'alice123' purchasing from seller 'mike87'
INSERT INTO carts (fk_buyer, fk_seller, fk_book, fk_state, fk_price, quantity) VALUES
    ('alice123', 'mike87', 28, 'new', 3500, 2),
    ('alice123', 'max_king', 4, 'new', 2050, 1),
    ('alice123', 'alex23', 20, 'as new', 1399, 1),
    ('alice123', 'chris99', 14, 'as new', 1200, 3);

-- Cart entry 2: Buyer 'bob_smith' purchasing from seller 'max_king'
INSERT INTO carts (fk_buyer, fk_seller, fk_book, fk_state, fk_price, quantity) VALUES
    ('bob_smith', 'max_king', 4, 'new', 2050, 1);

-- Cart entry 3: Buyer 'jane_doe' purchasing from seller 'chris99'
INSERT INTO carts (fk_buyer, fk_seller, fk_book, fk_state, fk_price, quantity) VALUES
    ('jane_doe', 'chris99', 14, 'as new', 1200, 2);


-- Add historical records to the 'history' table
INSERT INTO history (date, quantity, status, price, recensione, fk_buyer, fk_seller, fk_book, state) VALUES
    ('2023-01-20', 2, 'delivered', 1000, 'Great transaction!', 'alice123', 'mike87', 1, 'new'),
    ('2023-02-25', 3, 'shipped', 1000,  NULL, 'bob_smith', 'max_king', 4, 'as new'),
    ('2023-03-12', 4, 'on delivery', 1000, NULL, 'jane_doe', 'chris99', 11, 'new'),
    ('2023-04-05', 1, 'delivered', 1000, 'Smooth transaction.', 'sara_miller', 'alice123', 2, 'used'),
    ('2023-05-10', 2, 'delivered', 1000, 'Excellent service!', 'max_king', 'mike87', 3,'new'),
    ('2023-06-18', 3, 'shipped', 1000, NULL, 'emily_green', 'max_king', 5, 'as new'),
    ('2023-07-01', 4, 'on delivery', 1000, NULL, 'chris99', 'mike87', 6, 'used'),
    ('2023-08-14', 2, 'delivered', 1000, 'Book arrived in perfect condition.', 'lisa_wang', 'chris99', 7, 'used'),
    ('2023-09-22', 3, 'delivered', 1000, 'Fast shipping!', 'alex23', 'chris99', 8, 'as new'),
    ('2023-10-05', 1, 'delivered', 1000, 'Happy with the purchase.', 'alice123', 'chris99', 9, 'used');

