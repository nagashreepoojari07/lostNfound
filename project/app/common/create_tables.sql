-- Users Table
CREATE TABLE app_user (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email_id VARCHAR(500) NOT NULL UNIQUE,
    phone_no VARCHAR(10) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

-- Items table
CREATE TABLE lost_item (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES app_user(id),
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(50) CHECK (status IN ('MISSING','FOUND','RECEIVED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Status history table
CREATE TABLE status_history (
    id SERIAL PRIMARY KEY,
    item_id INT NOT NULL REFERENCES lost_item(id),
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    changed_by_user_id INT NOT NULL REFERENCES app_user(id),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

