

import mysql.connector

# DB connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="testdb"
)
cursor = db.cursor()

# table (run once)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
)
""")

# form data (example)
name = input("Enter name: ")
email = input("Enter email: ")

# insert data
cursor.execute(
    "INSERT INTO users (name, email) VALUES (%s, %s)",
    (name, email)
)
db.commit()

print("Data stored successfully")