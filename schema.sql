CREATE TABLE links (
    id serial PRIMARY KEY,
    id36 text UNIQUE,
    target text NOT NULL,
    created timestamp NOT NULL DEFAULT now(),
    created_by inet NOT NULL,
    active boolean NOT NULL DEFAULT TRUE
);