from db import db
from flask import session

def create_topic(topic_name):
    db.session.execute("INSERT INTO topics (topic_name, visible) VALUES (:topic_name, :visible)", {"topic_name":topic_name, "visible":True})
    db.session.commit()

def delete_topic(topic_id, user_id):
    if entitled_to_topics(user_id):
        db.session.execute("UPDATE topics SET visible=False WHERE id=:topic_id", {"topic_id": topic_id})
        db.session.commit()

def get_topics():
    topics = db.session.execute("SELECT topic_name, id FROM topics WHERE visible=:visible",{"visible": True} )
    return topics.fetchall()

def get_related_chains(topic_id):
    chains = db.session.execute(
        "SELECT chain_name, id FROM chains WHERE visible=:visible AND topic_id=:topic_id", {"visible": True, "topic_id": topic_id} )
    return chains.fetchall()

def get_topic_name(topic_id):
    name = db.session.execute(
        "SELECT topic_name FROM topics WHERE id=:topic_id", {"topic_id": topic_id})
    return name.fetchone()[0]

def entitled_to_topics(user_id):
    result = db.session.execute(
        "SELECT type from messages where id=:user_id", {"user_id": user_id})
    user_type = result.fetchone()
    return user_type == "admin"
