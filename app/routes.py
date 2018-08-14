import json

from flask import render_template, request, redirect, url_for, flash, Markup, jsonify

from kafka import KafkaConsumer, KafkaProducer

from app import app, db
# from app.models import User, UserQueries

#TODO: how about thread safety??
producer = KafkaProducer(
    bootstrap_servers=app.config['binoas']['zookeeper'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))


@app.route("/")
def index():
    return jsonify(app.config['binoas'])


@app.route("/posts/new")
def new_post():
    producer.send('topic', {
        'application': 'test',
        'payload': {
            'id': 1,
            'description': 'Dit is een test'
        }
    })
    return u''

if __name__ == "__main__":
    app.run(threaded=True)
