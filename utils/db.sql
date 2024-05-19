CREATE TABLE genres (
    name TEXT PRIMARY KEY
);

CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    first_name CHARACTER VARYING(255) NOT NULL,
    last_name CHARACTER VARYING(255) NOT NULL
);

CREATE TABLE publishers (
    name TEXT PRIMARY KEY
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    published DATE NOT NULL,
    pages INTEGER NOT NULL CONSTRAINT pages_gt CHECK (pages > 0),
    isbn CHARACTER VARYING(20),
    fk_author INTEGER,
    fk_publisher TEXT,
    FOREIGN KEY (fk_author) REFERENCES authors(id),
    FOREIGN KEY (fk_publisher) REFERENCES publishers(name)
);

CREATE TABLE booksgenres(
    fk_idB INTEGER,
    fk_genre TEXT,
    PRIMARY KEY (fk_idB, fk_genre),
    FOREIGN KEY (fk_idB) REFERENCES books(id),
    FOREIGN KEY (fk_genre) REFERENCES genres(name)
);

CREATE TABLE users(
    username VARCHAR(100) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    balance INTEGER NOT NULl CONSTRAINT balance_ge CHECK (balance >= 0),
    seller BOOLEAN NOT NULL,
    last_logged_in_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    token CHARACTER(64)[]
);

CREATE TYPE state AS ENUM ('new', 'as new', 'used');

CREATE TYPE status AS ENUM ('processing', 'packing', 'shipped', 'on delivery', 'delivered');

CREATE TABLE owns(
    id SERIAL PRIMARY KEY,
    fk_username VARCHAR(100),
    fk_book INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    state state NOT NULL,
    price INTEGER,
    UNIQUE (fk_username, fk_book, state, price),
    FOREIGN KEY (fk_username) REFERENCES users(username),
    FOREIGN KEY (fk_book) REFERENCES books(id)
);

CREATE TABLE carts(
    fk_buyer VARCHAR(100),
    fk_own INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (fk_buyer, fk_own),
    FOREIGN KEY (fk_buyer) REFERENCES users(username),
    FOREIGN KEY(fk_own) REFERENCES owns(id) ON DELETE CASCADE
);

CREATE TABLE history(
    id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    quantity INTEGER NOT NULL,
    status status NOT NULL,
    price INTEGER NOT NULL,
    review TEXT,
    fk_buyer VARCHAR(100),
    fk_seller VARCHAR(100),
    fk_book INTEGER,
    state state NOT NULL,
    FOREIGN KEY (fk_buyer) REFERENCES users(username),
    FOREIGN KEY (fk_seller) REFERENCES users(username),
    FOREIGN KEY (fk_book) REFERENCES books(id)
);

CREATE TABLE notifications(
    id SERIAL PRIMARY KEY,
    fk_order INTEGER NOT NULL,
    message TEXT NOT NULL,
    archived BOOLEAN NOT NULL,
    FOREIGN KEY (fk_order) REFERENCES history(id)
);

-- Trigger for Own.quantity

CREATE OR REPLACE FUNCTION remove_if_quantity_zero()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.quantity < 0 THEN
        RAISE EXCEPTION 'Quantity must be positive';
    ELSIF NEW.quantity = 0 THEN
        DELETE FROM owns WHERE id = NEW.id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_quantity_zero_trigger
AFTER UPDATE OF quantity ON owns
FOR EACH ROW
EXECUTE FUNCTION remove_if_quantity_zero();

-- Trigger for History.status

CREATE OR REPLACE FUNCTION notify_status_change() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO notifications (fk_order, message, archived)
    VALUES (OLD.id, 'Status changed to ' || NEW.status, FALSE);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_status_change
AFTER UPDATE ON history
FOR EACH ROW
WHEN (OLD.status IS DISTINCT FROM NEW.status)
EXECUTE FUNCTION notify_status_change();
