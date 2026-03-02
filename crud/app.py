from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="testdb"
)
cursor = db.cursor(dictionary=True)

# ---------- PRODUCTS CRUD (21,29,30) ----------
@app.route("/products", methods=["GET","POST"])
def products():
    if request.method == "POST":
        cursor.execute(
            "INSERT INTO products(name,price,category) VALUES(%s,%s,%s)",
            (request.form['name'], request.form['price'], request.form['category'])
        )
        db.commit()
        return redirect("/products")

    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()

    cursor.execute("SELECT category,COUNT(*) total FROM products GROUP BY category")
    grouped = cursor.fetchall()

    return render_template("products.html", products=data, grouped=grouped)

@app.route("/delete-products", methods=["POST"])
def bulk_delete_products():
    ids = request.form.getlist("ids")
    if ids:
        cursor.execute(
            f"DELETE FROM products WHERE id IN ({','.join(ids)})"
        )
        db.commit()
    return redirect("/products")


# ---------- EMPLOYEE SYSTEM (22–27) ----------
@app.route("/employees")
def employees():
    dept = request.args.get("dept")
    q = request.args.get("q")
    sort = request.args.get("sort")

    query = "SELECT * FROM employees WHERE 1"
    params = []

    if dept:
        query += " AND department=%s"
        params.append(dept)

    if q:
        query += " AND name LIKE %s"
        params.append('%'+q+'%')

    if sort:
        query += " ORDER BY salary " + sort

    cursor.execute(query, params)
    emp = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) total FROM employees")
    total = cursor.fetchone()['total']

    cursor.execute("SELECT * FROM employees ORDER BY salary DESC LIMIT 1")
    highest = cursor.fetchone()

    return render_template(
        "employees.html",
        employees=emp,
        total=total,
        highest=highest
    )


# ---------- MONTHLY STATS (28) ----------
@app.route("/stats")
def stats():
    cursor.execute("""
        SELECT MONTH(created_at) month, COUNT(*) total
        FROM users
        GROUP BY MONTH(created_at)
    """)
    data = cursor.fetchall()
    return render_template("stats.html", stats=data)


app.run(debug=True)