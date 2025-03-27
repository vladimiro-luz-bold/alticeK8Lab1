from flask import Flask, request, render_template, redirect, url_for, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB_HOST = os.getenv("DB_HOST", "db-service")
DB_NAME = os.getenv("DB_NAME", "demo_db")
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "password")

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if user:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials. Try again."
    
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return f"Welcome, {session['user']}! <br><a href='/logout'>Logout</a>"
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)