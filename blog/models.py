from utils.database import db, ma
from marshmallow import Schema, fields
from utils.base import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import validates


# Third-party libraries
from sqlalchemy.sql import select
import re



class Article(BaseModel):

    __tablename__ = 'articles'

    title = db.Column(db.String(32), index=True)
    author = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    body = db.Column(db.String(64000), nullable=False)
    image = db.Column(db.String, nullable=True)


    def __init__(self, title, body, author, image=None):
        self.title = title
        self.body = body
        self.author = author
        self.image = image

    @classmethod
    def get_article(cls, title=None, author=None, id_ =None):
        article = ''
        if title and author and id_:
            article = cls.query.filter_by(title=title, author=author)
        elif title and not author and not id_:
            user = cls.query.filter_by(title=title)
        elif author and not title and not id_:
            article = cls.query.filter_by(author=author)
        elif id and not title and not authpr:
            article = cls.query.filter_by(id=id)
        return article


    def __repr__(self):
        return f"<User: {self.title} {self.author}>"

    @validates('tile')
    def validate_title(self, key, title):
        if not title:
            raise AssertionError('No title provided')

        if self.get_user(title=title).first():
            raise AssertionError('Title is already in use')

        if len(title) < 5 or len(title) > 250:
            raise AssertionError(
                'Title must be between 5 and 250 characters')

        return username

    @validates('body')
    def validate_body(self, key, body):
        if not body:
            raise AssertionError('No body provided')

        if len(body) < 100:
            raise AssertionError('Article body must be more than 100 characters!')

        return body

    def validate_image(self, image):
        if not image:
            raise AssertionError('Image not provided')
        if not re.match(
            r'https?://(?:[-\w.]|(?:%[\da-fA-]{2}))+'
        , password):
            raise AssertionError(
                "Please provide a proper url!")

        return image


class ArticleSchema(Schema):
    class Meta:
        model = Article
        fields = ('title', 'body', 'author', 'image', 'created_at')
