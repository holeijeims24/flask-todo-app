from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    done INTEGER DEFAULT 0
)
""")

conn.commit()

tasks = []

@app.route("/")
def home():
   cursor.execute("SELECT id, task, done FROM tasks")
   rows = cursor.fetchall()

   total = len(rows)
   done_count = sum(row[2] for row in rows)
   left_count = total - done_count

   return render_template(
       "todo.html",
       tasks=rows,
       total=total,
       done_count=done_count,
       left_count=left_count
   )

@app.route("/add", methods=["POST"])
def add():
    task = request.form["task"]

    cursor.execute(
        "INSERT INTO tasks (task, done) VALUES (?, ?)",
        (task, 0)
    )
    conn.commit()

    return home()

@app.route("/delete/<int:id>")
def delete(id):
    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )
    conn.commit()

    return home()

@app.route("/done/<int:id>")
def done(id):
    cursor.execute(
        "UPDATE tasks SET done = 1 WHERE id = ?",
        (id,)
    )
    conn.commit()

    return home()

@app.route("/undone/<int:id>")
def undone(id):
    cursor.execute(
        "UPDATE tasks SET done = 0 WHERE id = ?",
        (id,)
    )
    conn.commit()

    return home()
    
app.run(debug=True)