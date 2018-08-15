import json
from functools import wraps

from flask import render_template, request, redirect, url_for, flash, Markup, jsonify
from kafka import KafkaConsumer, KafkaProducer

from app import app, BinoasError
from binoas.subscriptions import Subscription


def decode_json_post_data(fn):
    """Decorator that parses POSTed JSON and attaches it to the request
    object (:obj:`request.data`)."""

    @wraps(fn)
    def wrapped_function(*args, **kwargs):
        if request.method == 'POST':
            data = request.get_data(cache=False)
            if not data:
                raise BinoasError('No data was POSTed', 400)

            try:
                request_charset = request.mimetype_params.get('charset')
                if request_charset is not None:
                    data = json.loads(data, encoding=request_charset)
                else:
                    data = json.loads(data)
            except:
                raise BinoasError('Unable to parse POSTed JSON', 400)

            request.data = data

        return fn(*args, **kwargs)

    return wrapped_function

# TODO: how about thread safety??
producer = KafkaProducer(
    bootstrap_servers=app.config['binoas']['zookeeper'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))


@app.route("/")
def index():
    return jsonify(app.config['binoas'])


@app.route("/posts/new", methods=['POST'])
@decode_json_post_data
def new_post():
    if len(request.data.keys()) == 0:
        payload = {
            'application': 'test',
            'payload': {
                'id': 1,
                'description': 'Dit is een test',
                'topics': [
                    {'id': 1, 'name': 'tag1'},
                    {'id': 1, 'name': 'tag2'},
                ]
            }
        }
    else:
        payload = request.data

    producer.send('topic', payload)

    return jsonify({
        'status': 'ok'
    })


@app.route("/subscriptions/new", methods=['POST'])
@decode_json_post_data
def new_subscription():
    return jsonify(request.data)

if __name__ == "__main__":
    app.run(threaded=True)
