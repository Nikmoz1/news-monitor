import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
import os
from datetime import datetime
from sqlalchemy import create_engine, and_

basedir = os.path.abspath(os.path.dirname(__file__))

DB_URI = create_engine('sqlite:///' + os.path.join(basedir, 'app.db'), echo=True)
engine = DB_URI
Base = declarative_base(bind=engine)


class TelegramUser(Base):
    __tablename__ = "telegram_user"

    id = db.Column(db.Integer(), primary_key=True)
    is_bot = db.Column(db.Boolean(), default=False)
    first_name = db.Column(db.String(length=120))
    last_name = db.Column(db.String(length=120))
    username = db.Column(db.String(length=120))
    language_code = db.Column(db.String(length=10))
    referral_code = db.Column(db.String(length=64))
    parent_code = db.Column(db.String(length=64))
    steam_id = db.Column(db.Integer())
    region = db.Column(db.String(length=120))


class KeywordsUsers(Base):
    __tablename__ = "keywords"
    id = db.Column(db.Integer(), primary_key=True)
    keyword = db.Column(db.String(length=240))
    user_id = db.Column(db.Integer, db.ForeignKey('telegram_user.id'))
    is_active = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)


class DBDriver:
    # engine = engine

    @classmethod
    def is_new_user(cls, user_id):
        return cls.get_user(user_id) is None

    @classmethod
    def insert_user(cls, user_dict, parent_ref_code: str = None):
        with engine.connect() as connection:
            insert_query = db.insert(TelegramUser)
            if parent_ref_code:
                user_dict["parent_code"] = parent_ref_code
            connection.execute(insert_query, user_dict)

    @classmethod
    def get_user(cls, user_id):
        with engine.connect() as connection:
            result = connection.execute(
                db.select([TelegramUser]).where(TelegramUser.id == user_id)
            )
            data = list(map(dict, result))
            return data[0] if data else None

    @classmethod
    def add_keyword(cls, keyword):
        with engine.connect() as connection:
            if not keyword:
                return None
            insert_query = db.insert(KeywordsUsers)
            connection.execute(insert_query, keyword)

    @classmethod
    def remove_keyword(cls, keyword):
        with engine.connect() as connection:
            if not keyword:
                return None
            insert_query = db.delete(KeywordsUsers).where(and_(KeywordsUsers.keyword == keyword['keyword'],
                                                               KeywordsUsers.user_id == keyword['user_id']))
            connection.execute(insert_query, keyword)

    @classmethod
    def list_keyword(cls, user_id):
        with engine.connect() as connection:
            result = connection.execute(
                db.select([KeywordsUsers]).where(KeywordsUsers.user_id == user_id)
            )
            data = list(map(dict, result))
        return data


if __name__ == '__main__':
    Base.metadata.create_all()
