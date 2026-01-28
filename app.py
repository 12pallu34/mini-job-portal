from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------- DATABASE CONNECTION ----------
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------- HOME: SHOW JOBS ----------
@app.route("/")
def home():
    conn = get_db_connection()
    jobs = conn.execute("SELECT * FROM jobs").fetchall()
    conn.close()
    return render_template("index.html", jobs=jobs)

# ---------- ADMIN: ADD JOB ----------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        title = request.form["title"]
        company = request.form["company"]
        description = request.form["description"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO jobs (title, company, description) VALUES (?, ?, ?)",
            (title, company, description)
        )
        conn.commit()
        conn.close()

        return redirect("/admin")


    return render_template("admin.html")
# ---------- APPLY FOR JOB ----------
@app.route("/apply/<int:job_id>", methods=["GET", "POST"])
def apply(job_id):
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO applications (job_id, name, email) VALUES (?, ?, ?)",
            (job_id, name, email)
        )
        conn.commit()
        conn.close()

        return "Application submitted successfully!"

    return render_template("apply.html")



