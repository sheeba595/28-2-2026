from flask import Flask, render_template, request, redirect
import mysql.connector
import math

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="testdb"
)
cursor = db.cursor(dictionary=True)

@app.route("/students")
def students():
    q = request.args.get("q", "")
    page = int(request.args.get("page", 1))
    limit = 5
    offset = (page - 1) * limit

    if q:
        cursor.execute(
            "SELECT COUNT(*) total FROM students WHERE name LIKE %s",
            ('%' + q + '%',)
        )
        total = cursor.fetchone()['total']

        cursor.execute(
            "SELECT * FROM students WHERE name LIKE %s LIMIT %s OFFSET %s",
            ('%' + q + '%', limit, offset)
        )
    else:
        cursor.execute("SELECT COUNT(*) total FROM students")
        total = cursor.fetchone()['total']

        cursor.execute(
            "SELECT * FROM students LIMIT %s OFFSET %s",
            (limit, offset)
        )

    students = cursor.fetchall()
    pages = math.ceil(total / limit)

    return render_template(
        "students.html",
        students=students,
        q=q,
        page=page,
        pages=pages
    )

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    if request.method == "POST":
        cursor.execute(
            "UPDATE students SET name=%s,email=%s,course=%s WHERE id=%s",
            (
                request.form['name'],
                request.form['email'],
                request.form['course'],
                id
            )
        )
        db.commit()
        return redirect("/students")

    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()
    return render_template("edit_student.html", s=student)

@app.route("/delete/<int:id>")
def delete_student(id):
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    db.commit()
    return redirect("/students")

app.run(debug=True)


from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="testdb"
)
cursor = db.cursor()

# table (run once)
cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  message TEXT
)
""")

@app.route("/feedback", methods=["GET","POST"])
def feedback():
    if request.method == "POST":
        name = request.form['name']
        message = request.form['message']
        cursor.execute(
            "INSERT INTO feedback(name,message) VALUES(%s,%s)",
            (name, message)
        )
        db.commit()
        return redirect("/feedback")
    return render_template("feedback.html")

app.run(debug=True)

from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="testdb"
)
cursor = db.cursor()

# table (run once)
cursor.execute("""
CREATE TABLE IF NOT EXISTS contact (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  message TEXT
)
""")

@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        cursor.execute(
            "INSERT INTO contact(name,email,message) VALUES(%s,%s,%s)",
            (
                request.form['name'],
                request.form['email'],
                request.form['message']
            )
        )
        db.commit()
        return redirect("/contact")
    return render_template("contact.html")

app.run(debug=True)