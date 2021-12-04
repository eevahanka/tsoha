from flask import render_template, request, redirect
from flask import Flask
from os import getenv


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import users
import topics
import chains
import messages

@app.route("/")
def index():
    return render_template("index.html", username=users.username())

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/topics")
        else:
            return render_template("error.html", problem="kirjautuminen epäonnistui")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if len(username) == 0:
            return render_template("error.html", problem="anna käyttäjänimi")
        elif len(password1) == 0:
            return render_template("error.html", problem="anna salasana")
        elif password1 != password2:
            return render_template("error.html", problem = "salasanat eivät täsmää")
        elif users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", problem = "käyttäjänimi on jo käytössä")

@app.route("/topics")
def topics():
    return render_template("topics.html", topics=topics.get_topics())


@app.route("/topic/<int:id>")
def topic(id):
    return render_template("topic.html", chains=topics.get_related_chains(), topic_name=topics.get_topic_name(id))

@app.route("/chain/<int:id>")
def chain(id):
    return render_template("chain.html", messages=chains.get_related_messages(id), chain_name=chains.get_chain_name(id), topic_name=chains.get_topic_name(id)  )

@app.route("/message<int:id>")
def message(id):
    return render_template("message.html", content=messages.get_message_content(id), sender = messages.get_sender(id))

@app.route("/create_message", methods=["GET", "POST"])
def create_message(id):
    if request.method == "GET":
        return render_template("create_message.html")
    if request.method == "POST":
        content = request.form["message"]
        messages.create_message(users.user_id(), content, id )
        return render_template("chain.html", messages=chains.get_related_messages(id), chain_name=chains.get_chain_name(id), topic_name=chains.get_topic_name(id))


@app.route("/poll/<int:id>")
def poll(id):
    sql = "SELECT topic FROM polls WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    topic = result.fetchone()[0]
    sql = "SELECT id, choice FROM choices WHERE poll_id=:id"
    result = db.session.execute(sql, {"id": id})
    choices = result.fetchall()
    return render_template("poll.html", id=id, topic=topic, choices=choices)
