from collections import UserDict
import logging
import hashlib
import json

from binoas.db import setup_db
from binoas.es import setup_elasticsearch
from binoas.models import User, UserQueries


class Subscription(UserDict):
    """
    This is a simple class to represent an incoming subscription in the system.
    It checks upon initialization if the provided payload is in a correct
    format, Ie. if the expected keys are available.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (
            ('application' in self) and
            ('email' in self) and
            ('frequency' in self) and
            ('description' in self) and
            (
                ('subscription' in self) or
                ('query' in self)
            )
        ):
            raise ValueError('Not a valid subscription')

    def save(self, session):
        user = self.save_user(session)
        query = self.save_query(user, session)
        return user, query

    def save_user(self, session):
        user = session.query(User).filter_by(
            application=self['application'], email=self['email']).first()
        if user is None:
            user = User(
                application=self['application'],
                email=self['email']
            )
            session.add(user)
            session.commit()
        session
        return user

    def save_query(self, user, session):
        es = setup_elasticsearch()
        es_query = self.build_query()
        es_id = hashlib.sha224(
            ('%s:%s' % (
                self['application'],
                hashlib.sha224(json.dumps(es_query).encode('utf-8')
            ).hexdigest(),)).encode('utf-8')).hexdigest()

        # Index documents into new index
        index_name = 'binoas_%s' % (self['application'],)
        es.index(
            index=index_name, doc_type='queries', body=es_query, id=es_id)

        user_query = session.query(UserQueries).filter_by(
            user_id=user.id, query_id=es_id).first()
        if user_query is None:
            user_query = UserQueries(user_id=user.id, query_id=es_id)
            session.add(user_query)
        user_query.description = self['description']
        user_query.frequency = self['frequency']
        session.commit()
        return user_query


    def build_query(self):
        if 'query' in self:
            return self['query']
        else:
            return {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "term": {k: v}
                            } for k, v in self['subscription'].items()
                        ]
                    }
                }
            }
