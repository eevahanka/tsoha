CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT, 
    type TEXT
);
CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic_name TEXT, 
    visible BOOLEAN
);
CREATE TABLE chains (
    id SERIAL PRIMARY KEY, 
    chain_name TEXT,
    chain_message, TEXT
    creater_id INTEGER REFERENCES users,
    visible BOOLEAN,
    created_at TIMESTAMP,
    topic INTEGER REFERENCES topics 
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    sender INTEGER REFERENCES users,
    content TEXT,
    send_at TIMESTAMP,
    visible BOOLEAN,
    chain INTEGER REFERENCES chains
)

CREATE TABLE logins ( 
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    login_time TIMESTAMP
)