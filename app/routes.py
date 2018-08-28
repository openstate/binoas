import json
from functools import wraps
import logging

from flask import render_template, request, redirect, url_for, flash, Markup, jsonify
from kafka import KafkaConsumer, KafkaProducer

from app import app, BinoasError

from binoas.posts import Post
from binoas.subscriptions import Subscription
from binoas.mixins import ProducerMixin


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


class Producer(ProducerMixin):
    def __init__(self):
        """
        Initializes the process. The role is passed to give more information.
        """
        self.role = 'app'
        self.config = app.config

# TODO: how about thread safety??
producer = Producer()
producer.init_producer()

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

    try:
        post = Post(payload)
    except ValueError:
        raise BinoasError('Not a valid post payload', 400)

    producer.produce_message(payload)

    return jsonify({
        'status': 'ok'
    })


@app.route("/subscriptions/new", methods=['POST'])
@decode_json_post_data
def new_subscription():
    try:
        subscription = Subscription(request.data)
    except ValueError:
        raise BinoasError('Not a valid subscription payload', 400)

    try:
        user, user_query = subscription.save()
    except Exception as e:
        raise BinoasError('General error: %s' % (str(e),), 400)

    return jsonify({
        'status': 'ok',
        'user': {
            'id': user.id,
        },
        'query': {
            'id': user_query.query_id
        }
    })

if __name__ == "__main__":
    app.run(threaded=True)
