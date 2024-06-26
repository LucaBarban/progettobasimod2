CREATE DATABASE library;

CREATE USER librarian WITH PASSWORD 'test';

GRANT CONNECT ON DATABASE library TO librarian;

\c library

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
    FOREIGN KEY (fk_publisher) REFERENCES publishers(name),
    UNIQUE(isbn)
);

CREATE INDEX idx_title_books ON books(title);
CREATE INDEX idx_isbn_books ON books(isbn);
CREATE INDEX idx_author_books ON books(fk_author);
CREATE INDEX idx_publisher_books ON books(fk_publisher);

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
    balance INTEGER NOT NULL CONSTRAINT balance_ge CHECK (balance >= 0),
    seller BOOLEAN NOT NULL,
    last_logged_in_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    token CHARACTER(64)[]
);

CREATE INDEX idx_token_users ON users(token);

CREATE TYPE state AS ENUM ('new', 'as new', 'used');

CREATE TYPE status AS ENUM ('processing', 'packing', 'shipped', 'on delivery', 'delivered');

CREATE TABLE owns(
    id SERIAL PRIMARY KEY,
    fk_username VARCHAR(100),
    fk_book INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    state state NOT NULL,
    price INTEGER CONSTRAINT price_ge_owns CHECK (price >= 0),
    UNIQUE (fk_username, fk_book, state, price),
    FOREIGN KEY (fk_username) REFERENCES users(username),
    FOREIGN KEY (fk_book) REFERENCES books(id)
);

CREATE INDEX idx_own ON owns(fk_book, fk_username, state);

CREATE TABLE carts(
    fk_buyer VARCHAR(100),
    fk_own INTEGER NOT NULL,
    quantity INTEGER NOT NULL CONSTRAINT quantity_gt_carts CHECK (quantity > 0),
    PRIMARY KEY (fk_buyer, fk_own),
    FOREIGN KEY (fk_buyer) REFERENCES users(username),
    FOREIGN KEY(fk_own) REFERENCES owns(id) ON DELETE CASCADE
);

CREATE TABLE history(
    id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    quantity INTEGER NOT NULL CONSTRAINT quantity_gt_history CHECK (quantity > 0),
    status status NOT NULL,
    price INTEGER NOT NULL CONSTRAINT price_ge_history CHECK (price >= 0),
    review TEXT,
    stars INTEGER CONSTRAINT stars_btw CHECK (stars IS NULL OR stars BETWEEN 0 AND 5),
    fk_buyer VARCHAR(100),
    fk_seller VARCHAR(100),
    fk_book INTEGER,
    state state NOT NULL,
    FOREIGN KEY (fk_buyer) REFERENCES users(username),
    FOREIGN KEY (fk_seller) REFERENCES users(username),
    FOREIGN KEY (fk_book) REFERENCES books(id)
);

CREATE INDEX idx_history ON history(fk_buyer, fk_book, state, price);
CREATE INDEX idx_seller_history ON history(fk_seller);
CREATE INDEX idx_buyer_history ON history(fk_buyer);

CREATE TYPE disc_notif AS ENUM ('order updated');

CREATE TABLE notifications(
    id SERIAL PRIMARY KEY,
    context disc_notif NOT NULL,
    fk_username VARCHAR(100) NOT NULL,
    message TEXT,
    archived BOOLEAN NOT NULL,
    FOREIGN KEY (fk_username) REFERENCES users(username),

    -- Order
    fk_history INTEGER,
    order_status_old status,
    order_status_new status,
    FOREIGN KEY (fk_history) REFERENCES history(id)
);

CREATE INDEX idx_username_notifications ON notifications(fk_username);

CREATE MATERIALIZED VIEW notifications_count (username, count)
AS SELECT fk_username, COUNT(*) FROM notifications WHERE archived = false GROUP BY fk_username;

CREATE INDEX idx_username_notifications_count ON notifications_count(username);


CREATE MATERIALIZED VIEW star_count
AS
SELECT fk_seller, CAST(SUM(stars) AS DECIMAL)/COUNT(*) AS vote, COUNT(*) AS total FROM history
WHERE review IS NOT NULL
GROUP BY fk_seller
WITH NO DATA;

CREATE INDEX idx_seller_star_count ON star_count(fk_seller);


-- Trigger for Own.quantity
-- It's used to make some complex transactions fail, so do NOT substitute it with a CHECK constraint
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
AFTER INSERT OR UPDATE OF quantity ON owns
FOR EACH ROW
EXECUTE FUNCTION remove_if_quantity_zero();

-- Trigger for History.status

CREATE OR REPLACE FUNCTION notify_status_change()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO notifications (fk_username, context, archived, fk_history, order_status_old, order_status_new)
    VALUES (NEW.fk_buyer, 'order updated', FALSE, NEW.id, OLD.status, NEW.status);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_status_change
AFTER UPDATE ON history
FOR EACH ROW
WHEN (OLD.status IS DISTINCT FROM NEW.status)
EXECUTE FUNCTION notify_status_change();

-- Trigger for Notifications

CREATE OR REPLACE FUNCTION notifications_count_refresh()
RETURNS TRIGGER AS $$
BEGIN
    REFRESH MATERIALIZED VIEW notifications_count;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_notifications
AFTER INSERT OR UPDATE OR DELETE ON notifications
EXECUTE FUNCTION notifications_count_refresh();

-- Trigger for star_count

CREATE OR REPLACE FUNCTION refresh_star_count()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    REFRESH MATERIALIZED VIEW star_count;
    RETURN NULL;
END;
$$;

CREATE TRIGGER trigger_user_rating
AFTER INSERT OR UPDATE ON history
FOR EACH STATEMENT
EXECUTE PROCEDURE refresh_star_count();

-- Trigger for seller

CREATE OR REPLACE FUNCTION if_seller_is_seller()
RETURNS TRIGGER
AS $$
BEGIN
    IF EXISTS(
            SELECT 1
            FROM owns o join users u on o.fk_username = u.username
            WHERE o.id = NEW.fk_own AND u.seller
        ) THEN
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_carts_owner
BEFORE INSERT OR UPDATE ON carts
FOR EACH ROW
EXECUTE PROCEDURE if_seller_is_seller();

-- Trigger per carts

CREATE OR REPLACE FUNCTION check_selling()
RETURNS TRIGGER
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM owns
                WHERE id = NEW.fk_own AND price IS NOT NONE) THEN
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trigger_carts_selling
BEFORE INSERT OR UPDATE ON carts
FOR EACH ROW
EXECUTE FUNCTION check_selling();

-- Trigger for history notifications

CREATE OR REPLACE FUNCTION check_notification()
RETURNS TRIGGER
AS $$
BEGIN
    IF NEW.fk_history IS NOT NULL AND NOT EXISTS(
        SELECT 1 FROM history AS h
            WHERE h.id = NEW.fk_history AND
            NEW.fk_username = h.fk_buyer
            ) THEN
        RETURN NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trigger_history_notifications
BEFORE INSERT OR UPDATE ON notifications
FOR EACH ROW
EXECUTE FUNCTION check_notification();


-- Revoke unwanted privileges
REVOKE CREATE ON SCHEMA public FROM librarian;
REVOKE ALL PRIVILEGES ON DATABASE library FROM librarian;

-- Explicitly grant required privileges
GRANT CONNECT ON DATABASE library TO librarian;
GRANT USAGE ON SCHEMA public TO librarian;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO librarian;
GRANT SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO librarian;

ALTER TABLE notifications_count OWNER TO librarian;
ALTER TABLE star_count OWNER TO librarian;