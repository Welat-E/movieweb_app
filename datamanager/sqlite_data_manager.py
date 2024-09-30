from flask_sqlalchemy import SQLAlchemy

# Initialize the db instance from Flask-SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    """
    Represents a user in the database.
    """

    __tablename__ = "users"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return f"<User {self.name}>"


class Movie(db.Model):
    """
    Represents a movie in the database.
    """

    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    director = db.Column(db.String)
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    cover_image = db.Column(db.String)

    # Define a relationship between Movie and User
    user = db.relationship("User", backref=db.backref("movies", lazy=True))

    def __repr__(self):
        return f"<Movie {self.name}>"


class SQLiteDataManager:
    """
    Data manager to handle database operations.
    """

    def __init__(self, db_path):
        self.db_path = db_path

    def get_all_users(self):
        """
        Retrieves all users from the database.

        Returns:
            List of all users.
        """
        try:
            return User.query.all()
        except Exception as e:
            print(f"Error retrieving users: {e}")
            return []

    def get_user_movies(self, user_id):
        """
        Retrieves movies for a specific user.

        Args:
            user_id (int): The ID of the user whose movies are to be retrieved.

        Returns:
            List of movies for the specified user.
        """
        try:
            user = User.query.get(user_id)
            if user:
                return user.movies  # Access the related movies via the relationship
            else:
                return []
        except Exception as e:
            print(f"Error retrieving movies for user {user_id}: {e}")
            return []

    def add_user(self, user_id, name):
        """
        Adds a new user to the database.

        Args:
            user_id (int): The ID of the new user.
            name (str): The name of the new user.

        Returns:
            The new user object or None in case of failure.
        """
        try:
            new_user = User(id=user_id, name=name)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            print(f"Error adding user {name}: {e}")
            return None

    def add_movie(self, name, director, year, rating, user_id, cover_image):
        """
        Adds a new movie to the database for a specific user.

        Args:
            name (str): The name of the movie.
            director (str): The director of the movie.
            year (int): The year the movie was released.
            rating (float): The rating of the movie.
            user_id (int): The ID of the user who owns the movie.
            cover_image (str): The URL of the movie's cover image.

        Returns:
            The new movie object or None in case of failure.
        """
        try:
            new_movie = Movie(
                name=name,
                director=director,
                year=year,
                rating=rating,
                user_id=user_id,
                cover_image=cover_image,
            )
            db.session.add(new_movie)
            db.session.commit()
            return new_movie
        except Exception as e:
            print(f"Error adding movie {name}: {e}")
            return None

    def delete_movie(self, movie_id):
        """
        Deletes a movie from the database.

        Args:
            movie_id (int): The ID of the movie to be deleted.

        Returns:
            True if deletion was successful, False otherwise.
        """
        try:
            movie = Movie.query.get(movie_id)
            if movie:
                db.session.delete(movie)
                db.session.commit()
                return True
            return False
        except Exception as e:
            print(f"Error deleting movie {movie_id}: {e}")
            return False

    def delete_user(self, user_id):
        """
        Deletes a user from the database.

        Args:
            user_id (int): The ID of the user to be deleted.

        Returns:
            True if deletion was successful, False otherwise.
        """
        try:
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return True
            return False
        except Exception as e:
            print(f"Error deleting user {user_id}: {e}")
            return False


