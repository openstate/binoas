from collections import UserDict
import logging

from binoas.db import session
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
            (
                ('subscription' in self) or
                ('query' in self)
            )
        ):
            raise ValueError('Not a valid subscription')

    def save(self):
        raise NotImplementedError

    def save_user(self):
        user = session.query(User).filter_by(
            application=self['application'], email=self['email']).first()
        if user is None:
            user = User(
                application=self['application'],
                email=self['email']
            )
            session.add(user)
            session.commit()
