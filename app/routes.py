import json
from functools import wraps
import logging
import traceback

from flask import render_template, request, redirect, url_for, flash, Markup, jsonify
from kafka import KafkaConsumer, KafkaProducer

from app import app, BinoasError

from binoas.db import setup_db
from binoas.es import setup_elasticsearch
from binoas.posts import Post
from binoas.subscriptions import Subscription
from binoas.mixins import ProducerMixin
from binoas.models import UserQueries
from binoas.template import Templater
from binoas.mail import send_mail


def decode_json_post_data(fn):
    """Decorator that parses POSTed JSON and attaches it to the request
    object (:obj:`request.data`)."""

    @wraps(fn)
    def wrapped_function(*args, **kwargs):
        if request.method in ['POST', 'DELETE']:
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
                'description': 'Dit is een test met een aantal woorden er in',
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


@app.route("/posts/exists", methods=["POST"])
@decode_json_post_data
def exist_post():
    es = setup_elasticsearch(app.config)
    application = request.data.get('application', '')
    if application not in app.config['binoas']['applications'].keys():
        return jsonify({"status":"error","msg":"Illegal application"})

    application_index = 'binoas_%s' % (application,)
    ids = request.data.get('ids', [])
    existing = [i for i in request.data.get('ids', []) if es.exists(index=application_index, doc_type="item", id=i)]
    return jsonify({
            "new": list(Set(ids) - Set(existing)),
            "existing": existing
    })

@app.route("/subscriptions/new", methods=['POST'])
@decode_json_post_data
def new_subscription():
    result = {}
    session = setup_db(app.config)()
    try:
        subscription = Subscription(request.data)
    except ValueError:
        raise BinoasError('Not a valid subscription payload', 400)

    try:
        user, user_query = subscription.save(session)
        result = {
            'status': 'ok',
            'user': {
                'id': user.id,
            },
            'query': {
                'id': user_query.query_id
            }
        }
    except Exception as e:
        session.rollback()
        raise BinoasError('General error: %s' % (str(e),), 400)
    finally:
        session.close()

    transformed_message = {
        'application': subscription['application'],
        'payload': {
            'alerts': [
                {
                    'query': {
                        'id': user_query.query_id,
                        'description': subscription['description'],
                        'frequency': user_query.frequency
                    }
                }
            ],
            'user': {
                'id': user.id
            }
        }
    }

    try:
        templater = Templater(app.config)
        content = templater.compile(transformed_message, 'welcome')
        subject = templater.get_subject(transformed_message, 'welcome')

        send_mail(
            app.config['binoas']['sendgrid']['api_key'], subject, content,
            [subscription['email']])
    except Exception as e:
        l = "\n".join(traceback.format_exc().splitlines())
        raise BinoasError('General error upon mailing: %s (%s)' % (
            str(e),l,), 400)

    return jsonify(result)


@app.route("/subscriptions/delete", methods=['DELETE'])
@decode_json_post_data
def delete_subscription():
    user_id = request.data['user_id']
    query_id = request.data['query_id']
    session = setup_db(app.config)()
    es = setup_elasticsearch(app.config)

    uq = session.query(UserQueries).filter_by(
        user_id=user_id, query_id=query_id).first()
    if uq is not None:
        # delete from the database first.
        try:
            session.query(UserQueries).filter_by(
                user_id=user_id, query_id=query_id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise BinoasError('General error: %s' % (str(e),), 400)

    # now we need to find out if there are any user subscribed to this query
    # if not so, delete the query also.
    num_users = session.query(UserQueries).filter_by(
        query_id=query_id).count()
    if num_users <= 0:
        es.delete_by_query(index='_all', doc_type='queries', body={
          "query": {
            "term": {
              "_id": query_id
            }
          }
        })


    session.close()

    return jsonify({
        'status': 'ok'
    })


@app.route("/subscriptions", methods=["GET"])
@decode_json_post_data
def list_subscriptions():
    session = setup_db(app.config)()
    user_queries = session.query(UserQueries).filter_by(
        **request.args).all()
    results = {
        'meta': {
            'total': len(user_queries)
        },
        'results': [u.to_json() for u in user_queries]
    }
    session.close()
    return jsonify(results)

if __name__ == "__main__":
    app.run(threaded=True)
