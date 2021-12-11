from datetime import datetime
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from datetime import datetime

def login(username, password):
    result = db.session.execute("SELECT id, password FROM users WHERE username=:username", {"username": username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["csrf_token"] = secrets.token_hex(16)
            add_login_time()

            return True
        else:
            return False

def add_login_time():
    time =  datetime.now().strftime("%d.%m.%Y %H:%M")
    db.session.execute("INSERT INTO logins (user_id, login_time_timestamp, login_time) VALUES (:user_id, NOW(), :login_time)", {"user_id":user_id(), "login_time":time })
    db.session.commit()

def last_login():
    result = db.session.execute("SELECT login_time FROM logins WHERE user_id =:user_id ORDER BY login_time_timestamp DESC ", {"user_id": user_id()})
    try:
        last = result.fetchall()[1][0]
        return last
    except:
        return "edellistä kirjautumista ei ole tallennettu"

def logout():
    del session["user_id"]

def register(username, password):
    hash = generate_password_hash(password)
    try:
        db.session.execute("INSERT INTO users (username,password,type) VALUES (:username,:password,:type)", {
                           "username": username, "password": hash, "type": "user"})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def username():
    result = db.session.execute("SELECT username FROM users WHERE id=:id", {"id": user_id()})
    name = str(result.fetchone())[2:-3]   # result.fetchone()[0]
    return name

def is_admin():
    result = db.session.execute("SELECT type FROM users WHERE id=:id", {"id": user_id()})
    try:

        type = result.fetchone()[0]
        return type == 'admin'
    except:
        return False
