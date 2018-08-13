import os

# On a new deployment (whether production or development) make
# a copy of this file called 'config.py' and change 'False' for
# SECRET_KEY to a newly generated string using these python commands:
# $ import os
# $ os.urandom(24)

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = False
#    SERVER_NAME = 'waarismijnstemlokaal.nl'
#    PREFERRED_URL_SCHEME = 'https'
#    FORCE_HOST_FOR_REDIRECTS = 'waarismijnstemlokaal.nl'
#    USE_SESSION_FOR_NEXT = True

#    BABEL_DEFAULT_LOCALE = 'nl'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:<DB_PASSWORD>@stm_mysql_1:3306/binoas'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
