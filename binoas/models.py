from sqlalchemy.schema import PrimaryKeyConstraint

from app import app, db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application = db.Column(db.String(255), index=True)
    email = db.Column(db.String(255), index=True)


class UserQueries(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    query_id = db.Column(db.String(255), index=True)
    frequency = db.Column(db.String(255), index=True)

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'query_id'),
        {},
    )
