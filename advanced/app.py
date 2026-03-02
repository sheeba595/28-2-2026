from flask import Flask, render_template, request, redirect, session, send_file
import mysql.connector, csv, io
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="testdb"
)
cursor = db.cursor(dictionary=True)

# ---------- LOGIN / SESSION (31,32,33,34) ----------
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        cursor.execute(
            "SELECT * FROM users_login WHERE username=%s",
            (request.form['username'],)
        )
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], request.form['password']):
            session['user'] = user['username']
            session['role'] = user['role']
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

def login_required():
    if 'user' not in session:
        return redirect("/")

# ---------- DASHBOARD (36,40) ----------
@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect("/")

    cursor.execute("SELECT COUNT(*) total FROM employees")
    total_emp = cursor.fetchone()['total']

    cursor.execute("SELECT * FROM employees ORDER BY salary DESC LIMIT 1")
    highest = cursor.fetchone()

    return render_template(
        "dashboard.html",
        total=total_emp,
        highest=highest
    )

# ---------- PROFILE UPDATE (35) ----------
@app.route("/profile", methods=["GET","POST"])
def profile():
    if 'user' not in session:
        return redirect("/")

    if request.method == "POST":
        cursor.execute(
            "UPDATE users_login SET email=%s WHERE username=%s",
            (request.form['email'], session['user'])
        )
        db.commit()

    cursor.execute(
        "SELECT * FROM users_login WHERE username=%s",
        (session['user'],)
    )
    user = cursor.fetchone()
    return render_template("profile.html", user=user)

# ---------- SEARCH + FILTER (38) ----------
@app.route("/employees")
def employees():
    dept = request.args.get("dept")
    min_sal = request.args.get("min")
    max_sal = request.args.get("max")

    query = "SELECT * FROM employees WHERE 1"
    params = []

    if dept:
        query += " AND department=%s"
        params.append(dept)

    if min_sal and max_sal:
        query += " AND salary BETWEEN %s AND %s"
        params.extend([min_sal, max_sal])

    cursor.execute(query, params)
    data = cursor.fetchall()
    return render_template("employees.html", employees=data)

# ---------- EXPORT CSV (39) ----------
@app.route("/export")
def export():
    cursor.execute("SELECT * FROM employees")
    data = cursor.fetchall()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(data[0].keys())
    for row in data:
        writer.writerow(row.values())

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="employees.csv"
    )

app.run(debug=True)