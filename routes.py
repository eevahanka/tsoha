from app import app
from flask import render_template, request, redirect, session, abort
import messages
import users
import chains
import topics



@app.route("/")
def index():
    return render_template("index.html", username=users.username(), topics=topics.get_topics(), is_admin = users.is_admin(), last_login=users.last_login())

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
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

@app.route("/topic/<int:id>")
def topic(id):
    return render_template("topic.html", username=users.username(), chains=topics.get_related_chains(id), topic_name=topics.get_topic_name(id), id=id, csfr_token=session["csrf_token"])


@app.route("/chain/<int:id>")
def chain(id):
    return render_template("chain.html", username=users.username(), messages=chains.get_related_messages(id), chain_name=chains.get_chain_name(id), topic_name=chains.get_topic_name(id), id=id, topic_id=chains.get_related_topic(id), csfr_token=session["csrf_token"], is_entitled=chains.entitled_to_chain())


@app.route("/message/<int:id>", methods=["GET"])
def message(id):
    if request.method == "GET":
        return render_template("message.html", username=users.username(), content=messages.get_content(id), sender=messages.get_sender(id), id=id, chain_id=messages.get_related_chain(id))


#@app.route("/create_message", methods=["GET", "POST"])
#def create_message(chain_id):
#    if request.method == "GET":
#        return render_template("create_message.html")
#    if request.method == "POST":
#        content = request.form["message"]
#        messages.create_message(users.user_id(), content, chain_id)
#        return redirect("chain.html", username=users.username(), messages=chains.get_related_messages(chain_id), chain_name=chains.get_chain_name(chain_id), topic_name=chains.get_topic_name(chain_id))

@app.route("/create_chain", methods=["POST"])
def create_chain():
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        id = request.form["id"]
        chain_name = request.form["chain_name"]
        chain_message = request.form["chain_message"]
        chains.create_chain(chain_name, chain_message, users.user_id(), chains.get_related_topic(id))
        return redirect("/topic/" + str(id))


@app.route("/create_topic", methods=["POST"])
def create_topic():
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        print(0)
        if users.is_admin():
            topic_name = request.form["topic_name"]

            topics.create_topic(topic_name)
            print(1)
            return redirect("/")

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
    return redirect("/index")


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

