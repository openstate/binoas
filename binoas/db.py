from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = None
session = None


def setup_db(config):
    engine = create_engine(
        config['binoas']['db']['uri'], **config['binoas']['db']['options'])
    # use session_factory() to get a new Session
    _SessionFactory = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = _SessionFactory()
    return session
