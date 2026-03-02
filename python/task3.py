

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
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    course VARCHAR(100)
)
""")

# student registration
name = input("Student Name: ")
email = input("Email: ")
course = input("Course: ")

cursor.execute(
    "INSERT INTO students (name, email, course) VALUES (%s, %s, %s)",
    (name, email, course)
)
db.commit()

print("Student registered successfully")