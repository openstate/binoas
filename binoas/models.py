from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy import Integer, String, Column, ForeignKey

from binoas.db import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    application = Column(String(255), index=True)
    email = Column(String(255), index=True)


class UserQueries(Base):
    __tablename__ = 'user_queries'
    user_id = Column(Integer, ForeignKey("user.id"))
    query_id = Column(String(255), index=True)
    frequency = Column(String(255), index=True)

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'query_id'),
        {},
    )
