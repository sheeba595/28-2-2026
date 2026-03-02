
import mysql.connector
from getpass import getpass

# DB connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="testdb"
)
cursor = db.cursor(dictionary=True)

# table (run once)
cursor.execute("""
CREATE TABLE IF NOT EXISTS login (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(100)
)
""")

# ----- REGISTER (run once to add user) -----
# cursor.execute("INSERT INTO login(username,password) VALUES(%s,%s)", ("admin","12345"))
# db.commit()

# ----- LOGIN -----
username = input("Username: ")
password = getpass("Password: ")

cursor.execute(
    "SELECT * FROM login WHERE username=%s AND password=%s",
    (username, password)
)

user = cursor.fetchone()

if user:
    print("Login successful")
else:
    print("Invalid username or password")