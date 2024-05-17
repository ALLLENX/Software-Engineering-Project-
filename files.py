import sqlite3

def view_data():
    # Connect to the SQLite database
    with sqlite3.connect("hackathon_registration.db") as conn:
        cursor = conn.cursor()

        # Execute a SELECT query to view data
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        # Print the data
        for row in rows:
            print(row)

if __name__ == "__main__":
    view_data()
