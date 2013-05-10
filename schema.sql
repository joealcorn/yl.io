CREATE TABLE links (
    id serial PRIMARY KEY,
    id36 text UNIQUE NOT NULL,
    target text NOT NULL,
    created timestamp NOT NULL,
    created_by inet NOT NULL,
    active boolean NOT NULL
);