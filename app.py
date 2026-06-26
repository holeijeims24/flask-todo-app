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
messages = []

@app.route("/messages")
def messages_page():
    return render_template("messages.html")

@app.route("/message", methods=["POST"])
def message():
    text = request.form["text"]
    messages.append(text)

    result = "<h1>Повідомлення:</h1>"

    for msg in messages:
        result += f"<p>{msg}</p>"

    return result
    
app.run(debug=True)