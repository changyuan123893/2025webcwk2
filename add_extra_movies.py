from app import app, db
from models import Movie, Tag

# Extra example movies
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


def add_movies():
    with app.app_context():
        created = 0
        for em in extra_movies:
            exists = Movie.query.filter_by(title=em['title']).first()
            if exists:
                continue

            m = Movie(
                title=em['title'],
                year=em['year'],
                director=em['director'],
                rating=em['rating'],
                description=em['description']
            )

            # Add the movie to the session first
            db.session.add(m)
            for tag_name in em['tags']:
                tag = Tag.query.filter_by(name=tag_name).first()
                if tag:
                    m.tags.append(tag)
            created += 1

        if created > 0:
            db.session.commit()
        print(f"Added {created} example movies (if they did not exist).")


if __name__ == '__main__':
    add_movies()
