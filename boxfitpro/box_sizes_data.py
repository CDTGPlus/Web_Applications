import sqlite3
import random
import string
from werkzeug.security import generate_password_hash

def init_db():
    conn = sqlite3.connect('box_sizes.db')
    cursor = conn.cursor()

    # Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT NOT NULL,
            email TEXT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create Boxes Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS boxes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            length INTEGER NOT NULL,
            width INTEGER NOT NULL,
            height INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

def generate_random_username(base_username):
    random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    return f"{base_username}_{random_suffix}"

def add_user(account_name, email, username, password):
    conn = sqlite3.connect('box_sizes.db')
    cursor = conn.cursor()

    # Hash the password for security
    hashed_password = generate_password_hash(password)

    # Check if the username already exists
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        username = generate_random_username(username)

    # Add the user to the database
    cursor.execute('INSERT INTO users (account_name, email, username, password) VALUES (?, ?, ?, ?)', 
                   (account_name, email, username, hashed_password))
    conn.commit()
    conn.close()
    return username

# Function to add a box for a specific user
def add_box(user_id, length, width, height):
    conn = sqlite3.connect('box_sizes.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO boxes (user_id, length, width, height) VALUES (?, ?, ?, ?)',
                   (user_id, length, width, height))

    conn.commit()
    conn.close()

# Function to get all boxes for a specific user
def get_user_boxes(user_id):
    conn = sqlite3.connect('box_sizes.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM boxes WHERE user_id = ?', (user_id,))
    boxes = cursor.fetchall()

    conn.close()
    return boxes

# Function to update a box's dimensions
def update_box(box_id, length, width, height):
    conn = sqlite3.connect('box_sizes.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE boxes
        SET length = ?, width = ?, height = ?
        WHERE id = ?
    ''', (length, width, height, box_id))

    conn.commit()
    conn.close()

# Function to delete a box
def delete_box(box_id):
    conn = sqlite3.connect('box_sizes.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM boxes WHERE id = ?', (box_id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
