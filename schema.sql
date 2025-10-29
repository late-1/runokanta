CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE poems (
    id INTEGER PRIMARY KEY, 
    title TEXT,
    content TEXT,
    published DATE,
    user_id INTEGER REFERENCES users
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY, 
    poem_id INTEGER REFERENCES poems,
    user_id INTEGER REFERENCES users,
    rating INTEGER CHECK (rating >= 1 AND rating <= 10),
    comment TEXT,
    date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE category (
    id INTEGER PRIMARY KEY,
    poem_id INTEGER REFERENCES poems,
    title TEXT,
    value TEXT
);

CREATE TABLE themes (
    id INTEGER PRIMARY KEY,
    poem_id INTEGER REFERENCES poems,
    title TEXT,
    value TEXT
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    poem_id INTEGER REFERENCES poems,
    image BLOB
);