from db import db
from flask import session

def create_chain(chain_name, chain_message, creater_id, topic_id):

    db.session.execute(
        "INSERT INTO chains (chain_name, chain_message, creater_id, visible, created_at, topic_id) VALUES (:chain_name, :chain_message, :creater_id, :visible, NOW(), :topic_id )", {"chain_name":chain_name, "chain_message":chain_message, "creater_id":creater_id, "visible": True, "topic_id":topic_id }) 
    db.session.commit()

def delete_chain(chain_id, user_id):
    if entitled_to_chain(chain_id, user_id):
        db.session.execute("UPDATE chains SET visible=False WHERE id=:id", {"id": chain_id})
        db.session.commit()

def get_chains(topic_id):
    chains = db.session.execute("SELECT chain_name FROM chains WHERE visible=TRUE, topic_id=topic_id", {"topic_id": topic_id})
    return chains.fetchall()

def get_related_messages(chain_id):
    messages = db.session.execute(
        "SELECT messages.content, messages.sender_id, messages.id, users.username FROM messages LEFT JOIN users ON messages.sender_id = users.id WHERE visible= True AND messages.chain_id=chain_id", {"chain_id": chain_id})
    return messages.fetchall()

def get_chain_name(chain_id):
    name = db.session.execute(
        "SELECT chain_name FROM chains WHERE id=:chain_id", {"chain_id": chain_id})
    return name.fetchone()

def get_topic_name(chain_id):
    name = db.session.execute(
        "SELECT topics.topic_name FROM chains LEFT JOIN topics ON chains.topic_id = topics.id WHERE chains.id =:chain_id", {"chain_id": chain_id})
    return str(name.fetchone())[2:-3] #name.fetcone()[0]

def get_creater(chain_id):
    creater = db.session.execute(
        "SELECT users.username FROM chains LEFT JOIN users ON chains.creater_id = users.id WHERE chains-id = chain_id", {"chain_id": chain_id}
    )
    return creater.fetcone()[0]

def entitled_to_chain(chain_id, user_id):
    result = db.session.execute(
        "SELECT creater_id from chains where id=:chain_id", {
            "chain_id": chain_id}
    )
    creater_id = result.fetchone()
    result = db.session.execute(
        "SELECT type from users where id=:user_id", {"user_id": user_id}
    )
    user_type = result.fetchone()
    return user_id == creater_id or user_type == "admin"

def get_related_topic(chain_id):
    result = db.session.execute(
        "SELECT topic_id from chains WHERE id=:chain_id", {
            "chain_id": chain_id}
    )
    topic_id = result.fetchone()[0]
    return topic_id
