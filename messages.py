from ctypes import resize
from db import db
from flask import session

def create_message(sender_id, content, chain_id):
    db.session.execute("INSERT INTO messages (sender_id, content, send_at, visible, chain_id) VALUES (:sender_id, :content, NOW(), :visible, :chain_id) ", {"sender_id":sender_id, "content":content, "visible":True, "chain_id":chain_id})
    db.session.commit()


def delete_message(user_id, message_id):
    if entitled_to_message(message_id, user_id):

        db.session.execute("UPDATE messages SET visible=False WHERE id=:message_id", {"message_id":message_id})
        db.session.commit()

def get_content(message_id):
    content = db.session.execute(
        "SELECT content FROM messages WHERE id=:message_id", {"message_id": message_id})
    return content.fetchone()

def get_sender(message_id):
    sender = db.session.execute(
        "SELECT users.id, users.username FROM messages  LEFT JOIN users on messages.sender_id = users.id WHERE messages.id=:message_id", {"message_id": message_id})
    return sender.fetchone()

def entitled_to_message(message_id, user_id):
    print(0)
    result= db.session.execute(
        "SELECT sender_id from messages where id=:message_id", {
            "message_id": message_id}
    )
    sender_id = result.fetchone()[0]
    result = db.session.execute(
        "SELECT type from users where id=:user_id", {"user_id":user_id}
    )
    user_type = result.fetchone()[0]
    return user_id == sender_id or user_type == "admin"


def edit_message(message_id, user_id, new_content):
    if entitled_to_message(message_id, user_id):
        print(3)
        db.session.execute(
            "UPDATE messages SET content=:content WHERE id=:message_id", {"content": new_content, "message_id":message_id})
        db.session.commit()

def get_related_chain(message_id):
    result = db.session.execute(
        "SELECT chain_id from messages WHERE id=:message_id", {"message_id":message_id}
    )
    chain_id = result.fetchone()[0]
    return chain_id

