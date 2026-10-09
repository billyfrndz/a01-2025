import sqlite3
import os

os.makedirs('/app/data', exist_ok=True)
conn = sqlite3.connect('/app/data/lab.db')
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS notes;

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    role TEXT
);

CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    title TEXT,
    body TEXT
);

INSERT INTO users (username, password, role) VALUES
    ('admin',  'supersecret', 'admin'),
    ('alice',  'password123', 'user'),
    ('bob',    'hunter2',     'user');

INSERT INTO notes (user_id, title, body) VALUES
    (1, 'Admin secrets', 'The flag is: FLAG{r00t_0f_th3_l4b}'),
    (2, 'Alice note',    'Alice private data'),
    (3, 'Bob note',      'Bob private data');
""")

conn.commit()
conn.close()
print("DB initialized")