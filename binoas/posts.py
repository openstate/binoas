from collections import UserDict


class Post(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (
            ('application' in self) and
            ('payload' in self)
        ):
            raise ValueError('Not a valid post')
