import os
import re
from datetime import datetime
from pprint import pprint

import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from langdetect import detect

basedir = os.path.abspath(os.path.dirname(__file__))

engine = create_engine('sqlite:///' + os.path.join(basedir, 'news.db'), echo=True)
Base = declarative_base(bind=engine)

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


class News(Base):
    __tablename__ = 'news'

    # todo: визначити nullable поля
    id = db.Column(db.Integer(), primary_key=True)
    cluster_id = db.Column(db.String())
    source_name = db.Column(db.String(length=120))
    author = db.Column(db.String(length=120))
    title = db.Column(db.String(length=240))
    description = db.Column(db.String())
    partner_title = db.Column(db.String())
    url = db.Column(db.String())
    url_to_image = db.Column(db.String())
    date_created = db.Column(db.String(), default=datetime.now)
    content = db.Column(db.String())
    category = db.Column(db.String())
    language = db.Column(db.String())


# class PreparedNews(Base):
#     __tablename__ = "prepared_news"
#
#     # todo: додати відповідні поля
#     tonal_rating = db.Column(db.Integer)


class DBDriver:
    @classmethod
    def create_news(cls, news):
        with engine.connect() as connection:
            if not news:
                return None
            for elem in news:
                exists = session.query(db.exists().where((News.title == elem['title']))).scalar()

                if exists == False:
                    insert_query = db.insert(News)
                    language = detect(elem['title'])
                    connection.execute(insert_query, cluster_id=elem['cluster_id'],
                                       source_name=None,
                                       author=None,
                                       title=elem['title'],
                                       description=None,
                                       partner_title=elem['partner_title'],
                                       url=elem['url'],
                                       url_to_image=None,
                                       date_created=elem['date_created'],
                                       content=None,
                                       category=elem['category'],
                                       language=language)

    @classmethod
    def update_news(cls, dict_updates_news, title):
        with engine.connect() as connection:
            if not dict_updates_news or not title:
                return None

            connection.execute(db.update(News).where(News.title == title). \
                               values(dict_updates_news))

    @classmethod
    def read_news(cls, keyword):
        with engine.connect() as connection:
            if not keyword:
                return None

            news_title = connection.execute(db.select([News.id, News.title]))
            list_id_news = list()

            for row in news_title:
                text = str(row[1]).lower()
                keyword_lower = str(keyword).lower()

                if re.search(keyword_lower, text):
                    list_id_news.append(row[0])

            result = connection.execute(db.select([News]).where(News.id.in_(list_id_news)))

            data = list(map(dict, result))
            pprint(data)
            return data

    @classmethod
    def read_news_with_filter(cls, date_from, date_to):
        with engine.connect() as connection:
            if not date_from or not date_to:
                return None

            result = connection.execute(db.select([News]). \
                                        where(and_(News.date_created >= date_from, News.date_created <= date_to)))

            data = list(map(dict, result))
            return data


if __name__ == '__main__':
    Base.metadata.create_all(engine)
