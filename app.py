from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/hello", methods=["POST"])
def hello():
    name = request.form["name"]
    return f"<h1>Привіт, {name}!</h1>"

app.run(debug=True)