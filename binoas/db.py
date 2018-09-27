import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


Base = declarative_base()
engine = None
session = None


def setup_db(config={}):
    """
    Make a connection to the database, as specified in the configuration file.
    Returns the SQLAlchemy session factory.
    """
    global engine, session, Base

    if session is None:
        logging.info(
            'Setting up Database: %s' % (
                config['binoas']['db'],))
        engine = create_engine(
            config['binoas']['db']['uri'], **config['binoas']['db']['options'])
        # use session_factory() to get a new Session
        _SessionFactory = scoped_session(sessionmaker(bind=engine))
        Base.metadata.create_all(engine)
        session = _SessionFactory
    return session
