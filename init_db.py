from app import app, db
from models import Movie, Tag, User, Review
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random


def init_database():
    with app.app_context():
        db.drop_all()  # reset existing database
        db.create_all()

        print("Database tables created")

        # Seed genre tags
        tags_data = [
            'Action', 'Comedy', 'Romance', 'Sci-Fi', 'Horror',
            'Mystery', 'Animation', 'Documentary',
            'Adventure', 'Crime', 'Drama', 'Family', 'Fantasy',
            'History', 'Music', 'War',
            'Thriller', 'Western', 'Sports', 'Biography'
        ]

        tags = {}
        for tag_name in tags_data:
            tag = Tag(name=tag_name)
            db.session.add(tag)
            tags[tag_name] = tag

        db.session.commit()

        # Seed a fewfilms
        movies_data = [
            {
                'title': 'The Shawshank Redemption',
                'year': 1994,
                'director': 'Frank Darabont',
                'rating': 9.3,
                'description': 'After being convicted of a crime '
                               'he did not commit, '
                               'a banker forms an unlikely friendship while '
                               'planning a long game of survival and escape.',
                'tags': ['Drama', 'Crime']
            },
            {
                'title': 'Inception',
                'year': 2010,
                'director': 'Christopher Nolan',
                'rating': 8.8,
                'description': 'A skilled extractor enters people\'s '
                               'dreams to steal secrets and is tasked '
                               'with planting an idea instead.',
                'tags': ['Action', 'Sci-Fi', 'Mystery']
            },
            {
                'title': 'Titanic',
                'year': 1997,
                'director': 'James Cameron',
                'rating': 7.9,
                'description': 'A brief, tragic love story aboard '
                               'a ship that famously met an iceberg.',
                'tags': ['Romance', 'Drama']
            },
            {
                'title': 'Forrest Gump',
                'year': 1994,
                'director': 'Robert Zemeckis',
                'rating': 8.8,
                'description': 'The life of a kind-hearted man who, '
                               'despite limited expectations, '
                               'finds himself at the center of '
                               'historic moments.',
                'tags': ['Drama', 'Romance']
            },
            {
                'title': 'Interstellar',
                'year': 2014,
                'director': 'Christopher Nolan',
                'rating': 8.6,
                'description': 'Explorers travel through a wormhole '
                               'in search of a new home for humanity.',
                'tags': ['Sci-Fi', 'Adventure', 'Drama']
            },
            {
                'title': 'Avengers: Endgame',
                'year': 2019,
                'director': 'Anthony Russo, Joe Russo',
                'rating': 8.4,
                'description': 'The remaining heroes work together '
                               'to undo an act that cost '
                               'half the universe its inhabitants.',
                'tags': ['Action', 'Sci-Fi', 'Adventure']
            },
            {
                'title': 'Spirited Away',
                'year': 2001,
                'director': 'Hayao Miyazaki',
                'rating': 8.6,
                'description': 'A girl stumbles into a world of spirits '
                               'and must find her way back '
                               'while growing up fast.',
                'tags': ['Animation', 'Fantasy', 'Adventure']
            },
            {
                'title': 'The Godfather',
                'year': 1972,
                'director': 'Francis Ford Coppola',
                'rating': 9.2,
                'description': 'A powerful family patriarch transfers control '
                               'of his clandestine empire '
                               'to an unwilling son.',
                'tags': ['Crime', 'Drama']
            }
        ]

        movies = []
        for movie_data in movies_data:
            movie = Movie(
                title=movie_data['title'],
                year=movie_data['year'],
                director=movie_data['director'],
                rating=movie_data['rating'],
                description=movie_data['description']
            )

            # Attach tags to the movie
            for tag_name in movie_data['tags']:
                if tag_name in tags:
                    movie.tags.append(tags[tag_name])

            db.session.add(movie)
            movies.append(movie)

        db.session.commit()

        # Add additional example movies
        extra_movies = [
            {
                'title': 'movie_example1',
                'year': 2001,
                'director': 'director_example1',
                'rating': 7.1,
                'description': 'example description 1',
                'tags': ['Action', 'Adventure']
            },
            {
                'title': 'movie_example2',
                'year': 2002,
                'director': 'director_example2',
                'rating': 6.8,
                'description': 'example description 2',
                'tags': ['Comedy', 'Family', 'Drama']
            },
            {
                'title': 'movie_example3',
                'year': 2003,
                'director': 'director_example3',
                'rating': 7.5,
                'description': 'example description 3',
                'tags': ['Sci-Fi', 'Fantasy']
            },
            {
                'title': 'movie_example4',
                'year': 2004,
                'director': 'director_example4',
                'rating': 6.9,
                'description': 'example description 4',
                'tags': ['Thriller', 'Mystery']
            },
            {
                'title': 'movie_example5',
                'year': 2005,
                'director': 'director_example5',
                'rating': 7.3,
                'description': 'example description 5',
                'tags': ['Animation', 'Family']
            },
            {
                'title': 'movie_example6',
                'year': 2006,
                'director': 'director_example6',
                'rating': 7.0,
                'description': 'example description 6',
                'tags': ['Documentary', 'Biography', 'History']
            },
            {
                'title': 'movie_example7',
                'year': 2007,
                'director': 'director_example7',
                'rating': 6.7,
                'description': 'example description 7',
                'tags': ['Crime', 'Mystery']
            },
            {
                'title': 'movie_example8',
                'year': 2008,
                'director': 'director_example8',
                'rating': 7.6,
                'description': 'example description 8',
                'tags': ['Music', 'Drama']
            },
            {
                'title': 'movie_example9',
                'year': 2009,
                'director': 'director_example9',
                'rating': 6.5,
                'description': 'example description 9',
                'tags': ['History', 'Biography']
            }
        ]

        for em in extra_movies:
            m = Movie(
                title=em['title'],
                year=em['year'],
                director=em['director'],
                rating=em['rating'],
                description=em['description']
            )
            for tag_name in em['tags']:
                if tag_name in tags:
                    m.tags.append(tags[tag_name])
            db.session.add(m)

        db.session.commit()

        # Create test users
        if not User.query.filter_by(username='testuser').first():
            test_user = User(
                username='testuser',
                email='test@example.com',
                password_hash=generate_password_hash('password123')
            )
            db.session.add(test_user)

            # Create a second test account
            user2 = User(
                username='movielover',
                email='lover@example.com',
                password_hash=generate_password_hash('movielover123')
            )
            db.session.add(user2)

            db.session.commit()

            # Give the test usersfavorites
            for i in range(3):
                test_user.favorite_movies.append(movies[i])
                user2.favorite_movies.append(movies[i + 2])

            db.session.commit()

            # Add some example reviews
            reviews_data = [
                {
                    'user': test_user,
                    'movie': movies[0],
                    'rating': 5,
                    'content': 'A life-changing film with '
                               'many poignant moments.'
                },
                {
                    'user': test_user,
                    'movie': movies[1],
                    'rating': 4,
                    'content': 'Stunning visuals, though the plot '
                               'can be hard to follow at times.'
                },
                {
                    'user': user2,
                    'movie': movies[2],
                    'rating': 5,
                    'content': 'A classic romance that still moves me.'
                },
                {
                    'user': user2,
                    'movie': movies[3],
                    'rating': 5,
                    'content': 'Forrest Gump reminds us '
                               'how unexpected life can be.'
                }
            ]

            for review_data in reviews_data:
                review = Review(
                    content=review_data['content'],
                    rating=review_data['rating'],
                    user_id=review_data['user'].id,
                    movie_id=review_data['movie'].id,
                    created_at=datetime.utcnow() -
                    timedelta(days=random.randint(1, 30))
                )
                db.session.add(review)

            db.session.commit()

        print("Sample data added")
        print("=" * 50)
        print("Test accounts:")
        print("Username: testuser, Password: password123")
        print("Username: movielover, Password: movielover123")
        print("=" * 50)


if __name__ == '__main__':
    init_database()
