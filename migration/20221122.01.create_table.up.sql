CREATE TABLE company
(
    id         SERIAL PRIMARY KEY NOT NULL,
    name       VARCHAR(255)       NOT NULL,
    address    TEXT               NOT NULL,
    website    VARCHAR(255),
    scale      VARCHAR(50),
    slug       VARCHAR(255)       NOT NULL,
    contact    VARCHAR(255)       NOT NULL,
    created_at TIMESTAMP(6)       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP(6)       NOT NULL DEFAULT CURRENT_TIMESTAMP
);





