from app import app
from flask import render_template, request, redirect
import messages
import users
import chains
import topics

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
            return render_template("error.html", problem="salasanat eivät täsmää")
        elif users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", problem="käyttäjänimi on jo käytössä")


@app.route("/topics")
def topics_page():
    return render_template("topics.html", topics=topics.get_topics())


@app.route("/topic/<int:id>")
def topic(id):
    return render_template("topic.html", chains=topics.get_related_chains(id), topic_name=topics.get_topic_name(id), topic_id=id)


@app.route("/chain/<int:id>")
def chain(id):
    return render_template("chain.html", messages=chains.get_related_messages(id), chain_name=chains.get_chain_name(id), topic_name=chains.get_topic_name(id), id=id, topic_id=chains.get_related_topic(id))


@app.route("/message/<int:id>", methods=["GET"])
def message(id):
    if request.method == "GET":
        return render_template("message.html", content=messages.get_content(id), sender=messages.get_sender(id), id=id, chain_id=messages.get_related_chain(id))
    #if request.method == "POST":
    #    print(0)
    #    content = request.form["message"]
    #    chain_id = messages.get_related_chain(id)
    #    print(1)
    #    messages.edit_message(id, users.user_id(), content)
    #    print(2)
    #    return render_template(f"/chain.html/{chain_id}", messages=chains.get_related_messages(chain_id), chain_name=chains.get_chain_name(chain_id), topic_name=chains.get_topic_name(chain_id))


@app.route("/create_message", methods=["GET", "POST"])
def create_message(chain_id):
    if request.method == "GET":
        return render_template("create_message.html")
    if request.method == "POST":
        content = request.form["message"]
        messages.create_message(users.user_id(), content, chain_id)
        return redirect("chain.html", messages=chains.get_related_messages(chain_id), chain_name=chains.get_chain_name(chain_id), topic_name=chains.get_topic_name(chain_id))

@app.route("/delete_message/<int:id>")
def delete_message(id):
    chain_id = messages.get_related_chain(id)
    messages.delete_message(users.user_id(), id)
    return redirect(f"/chain/{chain_id}")

@app.route("/delete_chain/<int:id>")
def delete_chain(id):
    topic_id = chains.get_related_topic(id)
    chains.delete_chain(id, users.user_id())
    return redirect(f"/topic/{topic_id}")

@app.route("/delete_topic/<int:id>")
def delete_topic(id):
    topics.delete_topic(id, users.user_id())
    return redirect("/topics")


@app.route("/edit_message", methods=["POST"])
def edit_message():
    id = request.form["id"]
    chain_id = request.form["chain_id"]
    content = request.form["new_content"]
    chain_id = messages.get_related_chain(id)
    messages.edit_message(id, users.user_id(), content)
    return redirect("/chain/" + str(chain_id))


@app.route("/send_message", methods=["POST"])
def send_message():
    id = request.form["id"]
    content = request.form["content"]
    messages.create_message(users.user_id(), content, messages.get_related_chain(id))
    return redirect("/chain/" + str(id))

