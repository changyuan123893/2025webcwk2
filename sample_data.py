
TAGS = [
    'Action', 'Comedy', 'Romance',
    'Sci-Fi', 'Horror', 'Mystery', 'Animation', 'Documentary',
    'Adventure', 'Crime', 'Drama',
    'Family', 'Fantasy', 'History', 'Music', 'War',
    'Thriller', 'Western', 'Sports', 'Biography'
]

MOVIES_DATA = [
    {
        'title': 'The Shawshank Redemption',
        'year': 1994,
        'director': 'Frank Darabont',
        'rating': 9.3,
        'description': 'After being convicted of a crime he did not commit, '
                       'a banker forms an unlikely friendship '
                       'while planning a long game of survival and escape.',
        'tags': ['Drama', 'Crime']
    },
    {
        'title': 'Inception',
        'year': 2010,
        'director': 'Christopher Nolan',
        'rating': 8.8,
        'description': 'A skilled extractor enters people\'s dreams '
                       'to steal secrets and is tasked '
                       'with planting an idea instead.',
        'tags': ['Action', 'Sci-Fi', 'Mystery']
    },
    {
        'title': 'Titanic',
        'year': 1997,
        'director': 'James Cameron',
        'rating': 7.9,
        'description': 'A brief, tragic love story '
                       'aboard a ship that famously met an iceberg.',
        'tags': ['Romance', 'Drama']
    },
    {
        'title': 'Forrest Gump',
        'year': 1994,
        'director': 'Robert Zemeckis',
        'rating': 8.8,
        'description': 'The life of a kind-hearted man who, '
                       'despite limited expectations, '
                       'finds himself at the center of historic moments.',
        'tags': ['Drama', 'Romance']
    },
    {
        'title': 'Interstellar',
        'year': 2014,
        'director': 'Christopher Nolan',
        'rating': 8.6,
        'description': 'Explorers travel '
                       'through a wormhole in search of '
                       'a new home for humanity.',
        'tags': ['Sci-Fi', 'Adventure', 'Drama']
    },
    {
        'title': 'Avengers: Endgame',
        'year': 2019,
        'director': 'Anthony Russo, Joe Russo',
        'rating': 8.4,
        'description': 'The remaining heroes work together to '
                       'undo an act that cost half '
                       'the universe its inhabitants.',
        'tags': ['Action', 'Sci-Fi', 'Adventure']
    },
    {
        'title': 'Spirited Away',
        'year': 2001,
        'director': 'Hayao Miyazaki',
        'rating': 8.6,
        'description': 'A girl stumbles into a world of spirits '
                       'and must find her way back while growing up fast.',
        'tags': ['Animation', 'Fantasy', 'Adventure']
    },
    {
        'title': 'The Godfather',
        'year': 1972,
        'director': 'Francis Ford Coppola',
        'rating': 9.2,
        'description': 'A powerful family patriarch transfers '
                       'control of his clandestine '
                       'empire to an unwilling son.',
        'tags': ['Crime', 'Drama']
    }
]

# example movies used for incremental inserts
EXTRA_MOVIES = [
    {'title': 'movie_example1',
     'year': 2001,
     'director': 'director_example1',
     'rating': 7.1,
     'description': 'example description 1',
     'tags': ['Action', 'Adventure']},
    {'title': 'movie_example2',
     'year': 2002,
     'director': 'director_example2',
     'rating': 6.8,
     'description': 'example description 2',
     'tags': ['Comedy', 'Family', 'Drama']},
    {'title': 'movie_example3',
     'year': 2003,
     'director': 'director_example3',
     'rating': 7.5,
     'description': 'example description 3',
     'tags': ['Sci-Fi', 'Fantasy']},
    {'title': 'movie_example4',
     'year': 2004,
     'director': 'director_example4',
     'rating': 6.9,
     'description': 'example description 4',
     'tags': ['Thriller', 'Mystery']},
    {'title': 'movie_example5',
     'year': 2005,
     'director': 'director_example5',
     'rating': 7.3,
     'description': 'example description 5',
     'tags': ['Animation', 'Family']},
    {'title': 'movie_example6',
     'year': 2006,
     'director': 'director_example6',
     'rating': 7.0,
     'description': 'example description 6',
     'tags': ['Documentary', 'Biography', 'History']},
    {'title': 'movie_example7',
     'year': 2007,
     'director': 'director_example7',
     'rating': 6.7,
     'description': 'example description 7',
     'tags': ['Crime', 'Mystery']},
    {'title': 'movie_example8',
     'year': 2008,
     'director': 'director_example8',
     'rating': 7.6,
     'description': 'example description 8',
     'tags': ['Music', 'Drama']},
    {'title': 'movie_example9',
     'year': 2009,
     'director': 'director_example9',
     'rating': 6.5,
     'description': 'example description 9',
     'tags': ['History', 'Biography']},
    {'title': 'movie_example10',
     'year': 2010,
     'director': 'director_example10',
     'rating': 6.5,
     'description': 'example description 10',
     'tags': ['Family', 'Drama']},
]
