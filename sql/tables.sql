CREATE TABLE IF NOT EXISTS artist (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS album (
    id SERIAL PRIMARY KEY,
    artist_id INTEGER REFERENCES artist,
    name TEXT,
    genre TEXT,
    year INTEGER
);

CREATE TABLE IF NOT EXISTS reviewer (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password TEXT
);

CREATE TABLE IF NOT EXISTS review (
    id SERIAL PRIMARY KEY,
    reviewer_id INTEGER REFERENCES reviewer,
    album_id INTEGER REFERENCES album,
    rating INTEGER,
    comments TEXT
);

CREATE TABLE IF NOT EXISTS vote (
    id SERIAL PRIMARY KEY,
    review_id INTEGER REFERENCES review,
    reviewer_id INTEGER references reviewer,
    is_good BOOLEAN
);

CREATE TABLE IF NOT EXISTS follower (
    id SERIAL PRIMARY KEY,
    follower_id INTEGER references reviewer,
    followee_id INTEGER references reviewer
);
