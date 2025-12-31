from flask import (Flask, render_template, request,
                   redirect, url_for, jsonify, flash)
from flask_login import (LoginManager, login_user,
                         logout_user, login_required, current_user)
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Movie, Tag, Review
import logging
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    movies = Movie.query.order_by(Movie.rating.desc()).limit(6).all()
    return render_template('index.html', movies=movies)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not username or not email or not password:
            flash('All fields must be filled in.')
            return redirect(url_for('register'))

        if len(password) < 6:
            flash('The password must be at least 6 characters long.')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('The username already exists')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('The email has already been registered.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email,
                        password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        logger.info(f"New user registered: {username}")
        flash('Registration successful! Please log in')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = 'remember' in request.form

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            logger.info(f"User {username} logged in successfully")
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    logger.info(f"User {username} logged out")
    flash('Logged out')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    favorites = current_user.favorite_movies.limit(10).all()
    recommendations = get_recommendations(current_user)
    return render_template('dashboard.html',
                           favorites=favorites,
                           recommendations=recommendations)


@app.route('/profile')
@login_required
def profile():
    user_reviews = (Review.query.filter_by(user_id=current_user.id).
                    order_by(Review.created_at.desc()).limit(5).all())
    favorite_count = current_user.favorite_movies.count()
    return render_template('profile.html',
                           user=current_user,
                           reviews=user_reviews,
                           favorite_count=favorite_count)


@app.route('/movies')
def movies():
    tag_filter = request.args.get('tag')
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort', 'title')
    page = request.args.get('page', 1, type=int)
    per_page = 8

    query = Movie.query

    if tag_filter:
        query = query.filter(Movie.tags.any(Tag.name == tag_filter))

    if search_query:
        query = query.filter(Movie.title.ilike(f'%{search_query}%'))

    # Sorting
    if sort_by == 'rating':
        query = query.order_by(Movie.rating.desc())
    elif sort_by == 'year':
        query = query.order_by(Movie.year.desc())
    else:
        #  place example movies starting with "movie_example" at the end
        from sqlalchemy import case
        example_flag = case((Movie.title.ilike('movie_example%'), 1), else_=0)
        query = query.order_by(example_flag, Movie.title)

    # Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    movies = pagination.items
    tags = Tag.query.order_by(Tag.name).all()

    return render_template('movies.html', movies=movies, tags=tags,
                           pagination=pagination,
                           current_tag=tag_filter,
                           search_query=search_query, sort_by=sort_by)


@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    # Check whether user has favorited
    is_favorite = False
    user_review = None

    if current_user.is_authenticated:
        is_favorite = movie in current_user.favorite_movies
        user_review = Review.query.filter_by(
            user_id=current_user.id,
            movie_id=movie_id
        ).first()

    # Get all reviews
    reviews = (Review.query.filter_by(movie_id=movie_id).
               order_by(Review.created_at.desc()).all())

    return render_template('movie_detail.html',
                           movie=movie,
                           is_favorite=is_favorite,
                           user_review=user_review,
                           reviews=reviews)


@app.route('/favorite/<int:movie_id>', methods=['POST'])
@login_required
def toggle_favorite(movie_id):
    """Toggle favorite status - corrected version"""
    try:
        # Use raw SQL to ensure reliability
        from sqlalchemy import text

        # First check whether the movie exists
        movie = Movie.query.get(movie_id)
        if not movie:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'status': 'error',
                    'message': 'Movie does not exist'
                }), 404
            flash('Movie does not exist')
            return redirect(url_for('movies'))

        # Query association table directly to avoid ORM state issues
        check_sql = text("""
                         SELECT 1
                         FROM user_favorites
                         WHERE user_id = :user_id
                           AND movie_id = :movie_id
                         """)

        result = db.session.execute(
            check_sql,
            {'user_id': current_user.id, 'movie_id': movie_id}
        ).fetchone()

        # Decide action based on query result
        if result:
            # Remove favorite
            delete_sql = text("""
                              DELETE
                              FROM user_favorites
                              WHERE user_id = :user_id
                                AND movie_id = :movie_id
                              """)
            db.session.execute(delete_sql, {
                'user_id': current_user.id,
                'movie_id': movie_id
            })
            action = 'removed'
            action_display = 'Remove favorite'
            message = 'Removed from favorites'
            new_state = False
        else:
            # Add favorite
            insert_sql = text("""
                              INSERT INTO user_favorites
                                (user_id, movie_id, date_added)
                              VALUES (:user_id, :movie_id, :date_added)
                              """)
            db.session.execute(insert_sql, {
                'user_id': current_user.id,
                'movie_id': movie_id,
                'date_added': datetime.utcnow()
            })
            action = 'added'
            action_display = 'Add favorite'
            message = 'Added to favorites'
            new_state = True

        db.session.commit()

        # Recount
        count_sql = text("""
                         SELECT COUNT(*)
                         FROM user_favorites
                         WHERE movie_id = :movie_id
                         """)
        favorite_count = db.session.execute(
            count_sql, {'movie_id': movie_id}
        ).scalar()

        logger.info(f"User {current_user.username} "
                    f"{action_display} movie: {movie.title}")

        # Return JSON for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'status': 'success',
                'action': action,
                'action_display': action_display,
                'message': message,
                'new_state': new_state,
                'favorite_count': favorite_count,
                'movie_id': movie_id
            })

        # Only show Flash for non-AJAX (form) requests
        flash(message)
        return redirect(url_for('movie_detail', movie_id=movie_id))

    except Exception as e:
        db.session.rollback()
        logger.error(f"Favorite operation failed: {str(e)}")

        # Return JSON error for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'status': 'error',
                'message': 'Operation failed, please try again'
            }), 500

        # Only show Flash for non-AJAX requests
        flash('Operation failed, please try again')
        return redirect(url_for('movie_detail', movie_id=movie_id))


@app.route('/review/<int:movie_id>', methods=['POST'])
@login_required
def add_review(movie_id):
    content = request.form.get('content', '').strip()
    rating = request.form.get('rating', type=int)

    if not content or not rating:
        flash('Review content and rating cannot be empty')
        return redirect(url_for('movie_detail', movie_id=movie_id))

    if rating < 1 or rating > 5:
        flash('Rating must be between 1 and 5')
        return redirect(url_for('movie_detail', movie_id=movie_id))

    movie = Movie.query.get_or_404(movie_id)

    # Check whether a review already exists
    existing_review = Review.query.filter_by(
        user_id=current_user.id,
        movie_id=movie_id
    ).first()

    if existing_review:
        existing_review.content = content
        existing_review.rating = rating
        existing_review.created_at = datetime.utcnow()
        flash('Review updated')
    else:
        new_review = Review(
            content=content,
            rating=rating,
            user_id=current_user.id,
            movie_id=movie_id
        )
        db.session.add(new_review)
        flash('Review submitted')

    db.session.commit()
    logger.info(f"User {current_user.username} reviewed movie: {movie.title}")

    return redirect(url_for('movie_detail', movie_id=movie_id))


@app.route('/delete-review/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)

    if review.user_id != current_user.id:
        flash('You are not authorized to delete this review')
        return redirect(url_for('movie_detail', movie_id=review.movie_id))

    movie_id = review.movie_id
    db.session.delete(review)
    db.session.commit()

    logger.info(f"User {current_user.username} deleted review ID {review_id}")
    flash('Review deleted')

    return redirect(url_for('movie_detail', movie_id=movie_id))


@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', 'movie')

    if not query:
        flash('Please enter a search keyword')
        return redirect(url_for('movies'))

    if search_type == 'movie':
        results = Movie.query.filter(
            Movie.title.ilike(f'%{query}%') |
            Movie.description.ilike(f'%{query}%') |
            Movie.director.ilike(f'%{query}%')
        ).all()
    else:
        results = []

    return render_template('search_results.html',
                           results=results,
                           query=query,
                           search_type=search_type)


def get_recommendations(user):
    """Recommend based on user favorites"""
    user_favs = user.favorite_movies.all()

    if not user_favs:
        # If no favorites, return top-rated movies
        return Movie.query.order_by(Movie.rating.desc()).limit(6).all()

    # Recommend based on tags
    user_tags = {}
    for movie in user_favs:
        for tag in movie.tags:
            user_tags[tag.id] = user_tags.get(tag.id, 0) + 1

    if not user_tags:
        return Movie.query.filter(
            Movie.id.notin_([m.id for m in user_favs])
        ).order_by(Movie.rating.desc()).limit(6).all()

    # Find movies that share tags
    recommendations = []
    for movie in Movie.query.filter(
            Movie.id.notin_([m.id for m in user_favs])
    ).all():
        score = 0
        for tag in movie.tags:
            if tag.id in user_tags:
                score += user_tags[tag.id]

        if score > 0:
            recommendations.append((movie, score))

    # Sort by match score
    recommendations.sort(key=lambda x: x[1], reverse=True)
    recommended_movies = [movie for movie, score in recommendations[:6]]

    # If recommendations are insufficient, supplement with top-rated movies
    if len(recommended_movies) < 3:
        additional = (Movie.query.filter(
            Movie.id.notin_([m.id for m in user_favs])
        ).order_by(Movie.rating.desc()).
                      limit(6 - len(recommended_movies)).all())
        recommended_movies.extend(additional)

    return recommended_movies


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy',
                    'timestamp': datetime.utcnow().isoformat()})


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Initialize sample data (if the database is empty)
        if Movie.query.count() == 0:
            from init_db import init_database

            init_database()
            logger.info("Database initialized with sample data")

    app.run(debug=True, host='0.0.0.0', port=5000)
