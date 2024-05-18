import sqlite3

'''
you can edit and change tables based on your data
'''

def create_database():
    # Connect to SQLite database 
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the Hardware table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Hardware (
        Hardware_id INTEGER PRIMARY KEY
    )
    ''')

    # Create the Data table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Hardware_id INTEGER,
        Time TEXT,
        Date TEXT,
        Speed REAL,
        Label TEXT,
        Image BLOB,
        FOREIGN KEY (Hardware_id) REFERENCES Hardware (Hardware_id)
    )
    ''')

    print("Database and tables created successfully.")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Call the function 
create_database()
