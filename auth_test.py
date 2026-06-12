from flask import Flask, render_template, request, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "my_secret_key"

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    done INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    user_login TEXT NOT NULL
)
""")

conn.commit()

users = {
    "andriy": "1234",
    "nika": "5678"
}

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    login = request.form["login"]
    password = request.form["password"]

    cursor.execute(
        "SELECT * FROM users WHERE login = ? AND password = ?",
        (login, password)
    )

    user = cursor.fetchone()

    if user:
        session["login"] = login
        return f"<h1>Привіт, {login}!</h1>"

    return "<h1>Невірний логін або пароль</h1>"
@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    login = request.form["login"]
    password = request.form["password"]

    cursor.execute(
        "SELECT * FROM users WHERE login = ?",
        (login,)
    )

    user = cursor.fetchone()

    if user:
        return "<h1>Такий користувач вже існує</h1>"

    cursor.execute(
        "INSERT INTO users (login, password) VALUES (?, ?)",
        (login, password)
    )

    conn.commit()

    return f"<h1>Користувача {login} створено!</h1>"
@app.route("/profile")
def profile():
    if "login" in session:
        return f"<h1>Ти увійшов як {session['login']}</h1>"

    return "<h1>Ти не увійшов у систему</h1>"
@app.route("/tasks")
def tasks():
    if "login" not in session:
        return "<h1>Спочатку увійди в систему</h1>"
    search = request.args.get("search", "")
    filter_type = request.args.get("filter", "all")

    if filter_type == "active":
        cursor.execute(
            """
            SELECT id, task, done, created_at
            FROM tasks
            WHERE user_login = ? AND task LIKE ? AND done = 0
            ORDER BY id DESC
            """,
            (session["login"], f"%{search}%")
        )

    elif filter_type == "done":
        cursor.execute(
            """
            SELECT id, task, done, created_at
            FROM tasks
            WHERE user_login = ? AND task LIKE ? AND done = 1
            ORDER BY id DESC
            """,
            (session["login"], f"%{search}%")
        )

    else:
        cursor.execute(
            """
            SELECT id, task, done, created_at
            FROM tasks
            WHERE user_login = ? AND task LIKE ?
            ORDER BY done ASC, id DESC
            """,
            (session["login"], f"%{search}%")
        )

    rows = cursor.fetchall()

    total = len(rows)
    done_count = sum(row[2] for row in rows)
    left_count = total - done_count
    return render_template(
        "tasks.html",
        tasks=rows,
        login=session["login"],
        total=total,
        done_count=done_count,
        left_count=left_count,
        search=search
    )
@app.route("/add_task", methods=["POST"])
def add_task():
    if "login" not in session:
        return "<h1>Спочатку увійди в систему</h1>"

    task = request.form["task"]

    created_at = datetime.now().strftime("%d.%m.%Y %H:%M")

    cursor.execute(
        "INSERT INTO tasks (task, created_at, user_login) VALUES (?, ?, ?)",
        (task, created_at, session["login"])
)

    conn.commit()

    return tasks()
@app.route("/delete_task/<int:id>")
def delete_task(id):
    cursor.execute(
        "DELETE FROM tasks WHERE id = ? AND user_login = ?",
        (id, session["login"])
    )

    conn.commit()

    return tasks()
@app.route("/done_task/<int:id>")
def done_task(id):
    cursor.execute(
        "UPDATE tasks SET done = 1 WHERE id = ? AND user_login = ?",
        (id, session["login"])
    )

    conn.commit()

    return tasks()
@app.route("/undone_task/<int:id>")
def undone_task(id):
    cursor.execute(
        "UPDATE tasks SET done = 0 WHERE id = ? AND user_login = ?",
        (id, session["login"])
    )

    conn.commit()

    return tasks()
@app.route("/logout")
def logout():
    session.pop("login", None)
    return render_template("login.html")
@app.route("/edit_task/<int:id>")
def edit_task(id):
    cursor.execute(
        "SELECT task FROM tasks WHERE id = ? AND user_login = ?",
        (id, session["login"])
    )

    task = cursor.fetchone()

    if task is None:
        return "<h1>Завдання не знайдено</h1>"

    return render_template(
        "edit_task.html",
        id=id,
        task=task[0]
    )
@app.route("/update_task/<int:id>", methods=["POST"])
def update_task(id):
    new_task = request.form["task"]

    cursor.execute(
        "UPDATE tasks SET task = ? WHERE id = ? AND user_login = ?",
        (new_task, id, session["login"])
    )

    conn.commit()

    return tasks()

app.run(debug=True)