import json

from flask import render_template, request, redirect, url_for, flash, Markup, jsonify

from kafka import KafkaConsumer, KafkaProducer

from app import app

#TODO: how about thread safety??
producer = KafkaProducer(
    bootstrap_servers=app.config['binoas']['zookeeper'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))


@app.route("/")
def index():
    return jsonify(app.config['binoas'])


@app.route("/posts/new")
def new_post():
    producer.send('topic', {'a': 1})
    return u''

if __name__ == "__main__":
    app.run(threaded=True)
