from collections import UserDict
import logging


class Post(UserDict):
    """
    This is a simple class to represent a post in the system. It checks upon
    initialization if the provided payload is in a correct format, Ie. if the
    application and payload keys are available.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (
            ('application' in self) and
            ('payload' in self)
        ):
            raise ValueError('Not a valid post')
