from flask import render_template, request, redirect, url_for, flash, Markup, jsonify

from kafka import KafkaConsumer, KafkaProducer

from app import app

#TODO: how about thread safety??
producer = KafkaProducer(bootstrap_servers=app.config['binoas']['zookeeper'])


@app.route("/")
def index():
    return jsonify(app.config['binoas'])


@app.route("/posts/new")
def new_post():
    producer.send('topic', b"test")
    return u''

if __name__ == "__main__":
    app.run(threaded=True)
