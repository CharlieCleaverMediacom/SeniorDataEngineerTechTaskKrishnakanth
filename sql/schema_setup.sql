-- Users table
CREATE TABLE kk_users (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR(255),
    username VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    website VARCHAR(255)
);

-- Addresses table
CREATE TABLE kk_addresses (
    id SERIAL PRIMARY KEY,
    street VARCHAR(255),
    suite VARCHAR(100),
    city VARCHAR(100),
    zipcode VARCHAR(50),
    geo_lat DECIMAL(10, 6),
    geo_lng DECIMAL(10, 6),
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Companies table
CREATE TABLE kk_companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    catchphrase VARCHAR(255),
    bs VARCHAR(255),
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Posts table
CREATE TABLE kk_posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    title VARCHAR(255),
    body TEXT,
    status VARCHAR(50),
    created_at DATE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
