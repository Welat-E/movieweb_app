from flask import Flask, request, render_template, url_for, redirect, jsonify, abort
from datamanager.sqlite_data_manager import SQLiteDataManager, User, db, Movie
import requests
import creds

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/rojha/Desktop/Welat/movieweb_app/data/users_movies.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

data_manager = SQLiteDataManager("data/users_movies.sqlite")

@app.route('/')
def home():
    """Home page."""
    return "Welcome to MovieWeb App!"

@app.route('/users', methods=['GET'])
def list_users():
    """List all users."""
    try:
        users = data_manager.get_all_users()
        return render_template('users.html', users=users)
    except Exception as e:
        return render_template('500.html'), 500

@app.route('/users/<int:user_id>')
def get_user_movies(user_id):
    """List movies for a specific user."""
    try:
        movies = data_manager.get_user_movies(user_id)
        return render_template('user_movies.html', user_id=user_id, movies=movies)
    except Exception as e:
        return render_template('500.html'), 500

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Add a new user."""
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
            name = request.form['name']
            record = User(id=user_id, name=name)
            db.session.add(record)
            db.session.commit()
            return redirect(url_for('home'))
        except Exception as e:
            return render_template('500.html'), 500
    return render_template('add_user.html')

@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """Add a new movie for a specific user."""
    API_URL = "http://www.omdbapi.com/"

    if request.method == 'POST':
        title = request.form['name']
        params = {
            'apikey': creds.API_KEY,
            't': title
        }
        try:
            response = requests.get(API_URL, params=params)

            if response.status_code == 200:
                movie_data = response.json()
                if movie_data.get('Response') == 'True':
                    name = movie_data.get('Title')
                    director = movie_data.get('Director')
                    year = movie_data.get('Year')
                    rating = movie_data.get('imdbRating')

                    movie = Movie(
                        name=name,
                        director=director,
                        year=int(year) if year.isdigit() else None,
                        rating=float(rating) if rating else None,
                        user_id=user_id
                    )
                    db.session.add(movie)
                    db.session.commit()

                    return redirect(url_for('get_user_movies', user_id=user_id))
                else:
                    error_message = "Movie not found. Please try again."
                    return render_template('add_movie.html', user_id=user_id, error=error_message)
            else:
                error_message = "Error with the request. Please try again later."
                return render_template('add_movie.html', user_id=user_id, error=error_message)
        except Exception as e:
            return render_template('500.html'), 500

    return render_template('add_movie.html', user_id=user_id)

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """Update details of a specific movie for a user."""
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        try:
            new_title = request.form['name']
            new_director = request.form.get('director')
            new_year = request.form.get('year')
            new_rating = request.form.get('rating')

            movie.name = new_title
            movie.director = new_director
            movie.year = int(new_year) if new_year.isdigit() else None
            movie.rating = float(new_rating) if new_rating else None

            db.session.commit()
            return redirect(url_for('get_user_movies', user_id=user_id))
        except Exception as e:
            return render_template('500.html'), 500

    return render_template('update_movie.html', user_id=user_id, movie=movie)

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Delete a specific movie for a user."""
    try:
        movie = Movie.query.get_or_404(movie_id)
        db.session.delete(movie)
        db.session.commit()
        return redirect(url_for('get_user_movies', user_id=user_id))
    except Exception as e:
        return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors."""
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
