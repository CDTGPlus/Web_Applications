import sqlite3

def init_db():
    # Connect to the database
    conn = sqlite3.connect('box_sizes.db')
    cursor = conn.cursor()
    
    # Create the boxes table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS boxes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            length INTEGER NOT NULL,
            width INTEGER NOT NULL,
            height INTEGER NOT NULL
        )
    ''')
    
    # Insert some basic box sizes if the table is empty
    cursor.execute('SELECT * FROM boxes')
    if not cursor.fetchall():
        basic_boxes = [
            (10, 10, 10),
            (15, 15, 15),
            (20, 20, 20),
            (25, 25, 25),
            (30, 30, 30)
        ]
        cursor.executemany('INSERT INTO boxes (length, width, height) VALUES (?, ?, ?)', basic_boxes)
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized and box sizes added (if they didn't already exist).")
