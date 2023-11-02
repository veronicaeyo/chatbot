import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the tasks table if it doesn't exist
cursor.execute(
    """CREATE TABLE IF NOT EXISTS tasks
             (id SERIAL PRIMARY KEY,
             task TEXT NOT NULL,
             completed BOOLEAN,
             due_date DATE,
             completion_date DATE,
             priority INTEGER)"""
)

# Insert sample tasks into the tasks table
cursor.execute(
    "INSERT INTO tasks (task, completed, due_date, completion_date, priority) VALUES (%s, %s, %s, %s, %s)",
    ("Complete the web page design", True, "2023-05-01", "2023-05-03", 1),
)
cursor.execute(
    "INSERT INTO tasks (task, completed, due_date, completion_date, priority) VALUES (%s, %s, %s, %s, %s)",
    ("Create login and signup pages", True, "2023-05-03", "2023-05-05", 2),
)
cursor.execute(
    "INSERT INTO tasks (task, completed, due_date, completion_date, priority) VALUES (%s, %s, %s, %s, %s)",
    ("Product management", False, "2023-05-05", None, 3),
)
cursor.execute(
    "INSERT INTO tasks (task, completed, due_date, completion_date, priority) VALUES (%s, %s, %s, %s, %s)",
    ("Cart and wishlist creation", False, "2023-05-08", None, 4),
)
cursor.execute(
    "INSERT INTO tasks (task, completed, due_date, completion_date, priority) VALUES (%s, %s, %s, %s, %s)",
    ("Payment gateway integration", False, "2023-05-10", None, 5),
)
cursor.execute(
    "INSERT INTO tasks (task, completed, due_date, completion_date, priority) VALUES (%s, %s, %s, %s, %s)",
    ("Order management", False, "2023-05-10", None, 6),
)

# cursor.execute("SELECT * FROM tasks")

# rows = cursor.fetchall()
# for row in rows:
#     print(row)

# Commit the changes and close the connection
conn.commit()
conn.close()
