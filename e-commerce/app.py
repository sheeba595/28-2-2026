from flask import Flask, render_template, request, redirect, session
import mysql.connector, os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="testdb"
)
cursor = db.cursor(dictionary=True)

# ---------- LOGIN / LOGOUT (49) ----------
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        cursor.execute("SELECT * FROM users WHERE username=%s",
                       (request.form['username'],))
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], request.form['password']):
            session['user'] = user['username']
            session['role'] = user['role']
            session['cart'] = []
            return redirect("/products")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------- PRODUCT LISTING (41) ----------
@app.route("/products")
def products():
    cursor.execute("SELECT * FROM products")
    return render_template("products.html", products=cursor.fetchall())

# ---------- CART (42,43) ----------
@app.route("/add/<int:id>")
def add_to_cart(id):
    session['cart'].append(id)
    return redirect("/products")

@app.route("/cart")
def cart():
    items, total = [], 0
    for pid in session['cart']:
        cursor.execute("SELECT * FROM products WHERE id=%s", (pid,))
        p = cursor.fetchone()
        items.append(p)
        total += p['price']
    return render_template("cart.html", items=items, total=total)

# ---------- ORDERS (44,45) ----------
@app.route("/place-order")
def place_order():
    total = 0
    for pid in session['cart']:
        cursor.execute("SELECT price FROM products WHERE id=%s", (pid,))
        total += cursor.fetchone()['price']

    cursor.execute(
        "INSERT INTO orders(username,total) VALUES(%s,%s)",
        (session['user'], total)
    )
    db.commit()
    session['cart'] = []
    return redirect("/orders")

@app.route("/orders")
def orders():
    cursor.execute("SELECT * FROM orders WHERE username=%s",
                   (session['user'],))
    return render_template("orders.html", orders=cursor.fetchall())

# ---------- ADMIN + IMAGE UPLOAD (46,47) ----------
@app.route("/admin", methods=["GET","POST"])
def admin():
    if session.get("role") != "Admin":
        return redirect("/")

    if request.method == "POST":
        img = request.files['image']
        path = UPLOAD_FOLDER + "/" + img.filename
        img.save(path)
        cursor.execute(
            "INSERT INTO products(name,price,image) VALUES(%s,%s,%s)",
            (request.form['name'], request.form['price'], path)
        )
        db.commit()

    cursor.execute("SELECT * FROM products")
    return render_template("admin.html", products=cursor.fetchall())

# ---------- DASHBOARD STATS (48) ----------
@app.route("/dashboard")
def dashboard():
    cursor.execute("SELECT COUNT(*) c FROM users")
    users = cursor.fetchone()['c']
    cursor.execute("SELECT COUNT(*) c FROM products")
    products = cursor.fetchone()['c']
    cursor.execute("SELECT COUNT(*) c FROM orders")
    orders = cursor.fetchone()['c']
    return render_template("dashboard.html",
                           users=users, products=products, orders=orders)

app.run(debug=True)