# Import necessary modules and initialize the Flask app
from flask import Flask, flash, request, render_template, url_for, redirect, jsonify, abort
from datamanager.sqlite_data_manager import SQLiteDataManager, User, db, Movie
import requests
import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


app = Flask(__name__)
app.secret_key = '1223901'
load_dotenv()
API_KEY = os.environ.get("API_KEY")

# Configure the app with SQLite database

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:////Users/welat/Desktop/movieweb_app/data/users_movies.sqlite"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Initialize data manager
data_manager = SQLiteDataManager("data/users_movies.sqlite")


# Home route
@app.route("/")
def home():
    """
    Renders the home page.

    Method: GET

    Returns:
        A rendered HTML template for the home page.
    """
    users = User.query.all()
    return render_template("home.html", users=users)


# List users
@app.route("/users", methods=["GET"])
def list_users():
    """
    Lists all users in the system.

    Method: GET

    Returns:
        A rendered HTML template displaying the list of users or a 500 error page in case of failure.
    """
    try:
        users = data_manager.get_all_users()
        return render_template("users.html", users=users)
    except Exception as e:
        return render_template("500.html"), 500


# Get user movies
@app.route("/users/<int:user_id>")
def get_user_movies(user_id):
    """
    Displays the movies for a specific user.

    Method: GET

    Args:
        user_id (int): The ID of the user whose movies are to be displayed.

    Returns:
        A rendered HTML template with the user's movie list or a 500 error page in case of failure.
    """
    try:
        movies = data_manager.get_user_movies(user_id)
        return render_template("user_movies.html", user_id=user_id, movies=movies)
    except Exception as e:
        return render_template("500.html"), 500


# Add a new user
@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    """
    Adds a new user to the system.

    Method: GET, POST

    Returns:
        GET: A rendered HTML form for adding a user.
        POST: Redirects to the home page or displays a 500 error page in case of failure.
    """
    if request.method == "POST":
        try:
            user_id = request.form["user_id"]
            name = request.form["name"]
            record = User(id=user_id, name=name)
            db.session.add(record)
            db.session.commit()
            return redirect(url_for("home"))
        except Exception as e:
            return render_template("500.html"), 500
    return render_template("add_user.html")


# Add a new movie for a user
@app.route("/users/<int:user_id>/add_movie", methods=["GET", "POST"])
def add_movie(user_id):
    """
    Adds a new movie for a specific user by fetching data from the OMDB API.

    Method: GET, POST

    Args:
        user_id (int): The ID of the user for whom the movie is being added.

    Returns:
        GET: A rendered HTML form for adding a movie.
        POST: Redirects to the user's movie list page or displays an error message in case of failure.
    """
    API_URL = "http://www.omdbapi.com/"

    if request.method == "POST":
        title = request.form["name"]
        params = {"apikey": API_KEY, "t": title}
        try:
            response = requests.get(API_URL, params=params)
            if response.status_code == 200:
                movie_data = response.json()
                if movie_data.get("Response") == "True":
                    name = movie_data.get("Title")
                    director = movie_data.get("Director")
                    year = movie_data.get("Year")
                    rating = movie_data.get("imdbRating")

                    movie = Movie(
                        name=name,
                        director=director,
                        year=int(year) if year.isdigit() else None,
                        rating=float(rating) if rating else None,
                        user_id=user_id,
                    )
                    db.session.add(movie)
                    db.session.commit()

                    return redirect(url_for("get_user_movies", user_id=user_id))
                else:
                    error_message = "Movie not found. Please try again."
                    return render_template(
                        "add_movie.html", user_id=user_id, error=error_message
                    )
            else:
                error_message = "Error with the request. Please try again later."
                return render_template(
                    "add_movie.html", user_id=user_id, error=error_message
                )
        except Exception as e:
            return render_template("500.html"), 500

    return render_template("add_movie.html", user_id=user_id)


# Update a movie for a user
@app.route("/users/<int:user_id>/update_movie/<int:movie_id>", methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    """
    Updates the details of a specific movie for a user.

    Method: GET, POST

    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie to be updated.

    Returns:
        GET: A rendered HTML form to update movie details.
        POST: Redirects to the user's movie list page or a 500 error page in case of failure.
    """
    movie = Movie.query.get_or_404(movie_id)

    if request.method == "POST":
        try:
            new_title = request.form["name"]
            new_director = request.form.get("director")
            new_year = request.form.get("year")
            new_rating = request.form.get("rating")

            movie.name = new_title
            movie.director = new_director
            movie.year = int(new_year) if new_year.isdigit() else None
            movie.rating = float(new_rating) if new_rating else None

            db.session.commit()
            return redirect(url_for("get_user_movies", user_id=user_id))
        except Exception as e:
            return render_template("500.html"), 500

    return render_template("update_movie.html", user_id=user_id, movie=movie)


# Delete a movie for a user
@app.route("/users/<int:user_id>/delete_movie/<int:movie_id>", methods=["POST"])
def delete_movie(user_id, movie_id):
    """
    Deletes a specific movie for a user.

    Method: POST

    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie to be deleted.

    Returns:
        Redirects to the user's movie list page or a 500 error page in case of failure.
    """
    try:
        movie = Movie.query.get_or_404(movie_id)
        db.session.delete(movie)
        db.session.commit()
        return redirect(url_for("get_user_movies", user_id=user_id))
    except Exception as e:
        return render_template("500.html"), 500


@app.route('/delete_user/<string:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    
    if user:  #check if user exists
        db.session.delete(user)
        db.session.commit()
    else:
        return "User not found", 404

    return redirect(url_for('home'))



# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    """
    Handles 404 Not Found errors.

    Returns:
        A rendered 404 error page.
    """
    return render_template("404.html"), 404


# Handle 500 errors
@app.errorhandler(500)
def internal_server_error(e):
    """
    Handles 500 Internal Server errors.

    Returns:
        A rendered 500 error page.
    """
    return render_template("500.html"), 500


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
