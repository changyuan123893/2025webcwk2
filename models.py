from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# Many-to-many relationship table
# Movies favorited by users
user_favorites = db.Table('user_favorites',
                          db.Column('user_id', db.Integer,
                                    db.ForeignKey('user.id')),
                          db.Column('movie_id', db.Integer,
                                    db.ForeignKey('movie.id')),
                          db.Column('date_added', db.DateTime,
                                    default=datetime.utcnow)
                          )

# Movie tags
movie_tags = db.Table('movie_tags',
                      db.Column('movie_id', db.Integer,
                                db.ForeignKey('movie.id')),
                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                      )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Movies favorited by users
    favorite_movies = db.relationship('Movie',
                                      secondary=user_favorites,
                                      back_populates='favorited_by',
                                      lazy='dynamic')

    # One-to-many relationship: User's comments
    reviews = db.relationship('Review', backref='author', lazy=True)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer)
    director = db.Column(db.String(100))
    description = db.Column(db.Text)
    rating = db.Column(db.Float)
    poster_url = db.Column(db.String(500))

    # Many-to-many: Users who have favorited this movie
    favorited_by = db.relationship('User',
                                   secondary=user_favorites,
                                   back_populates='favorite_movies',
                                   lazy='dynamic')

    # Many-to-many: tags of movies
    tags = db.relationship('Tag',
                           secondary=movie_tags,
                           back_populates='movies')

    # One-to-many: reviews of movies
    reviews = db.relationship('Review', backref='movie', lazy=True)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Many-to-many: movies with this tag
    movies = db.relationship('Movie',
                             secondary=movie_tags,
                             back_populates='tags')


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)  # 1-5星
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
