from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from binoas.db import Base


class User(Base):
    """
    This represent a 'user' in the system. A user is unique within
    an application, as defined in the configuration file.
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    application = Column(String(255), index=True)
    email = Column(String(255), index=True)

    queries = relationship("UserQueries", back_populates="user")


class UserQueries(Base):
    """
    This represents the queries that a particular user has subscribed to. It
    refers to the user table using the user_id column. The query_id Column
    is used to make a link to the query as stored in Elasticsearch.
    """
    __tablename__ = 'user_queries'
    user_id = Column(Integer, ForeignKey("user.id"))
    description = Column(String(255))
    query_id = Column(String(255), index=True)
    frequency = Column(String(255), index=True)

    user = relationship("User", back_populates="queries")

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'query_id'),
        {},
    )
