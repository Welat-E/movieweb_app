
# SQLAlchemy model and data manager for SQLite database interactions
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from datamanager.data_manager_interface import DataManagerInterface

db = SQLAlchemy()


# Define the User model for the database
class User(db.Model):
    """
    Represents a user in the database.
    """
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)


# Define the Movie model for the database
class Movie(db.Model):
    """
    Represents a movie in the database.
    """
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    director = db.Column(db.String)
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    user_id = db.Column(db.Integer)


# SQLite-based data manager that implements DataManagerInterface
class SQLiteDataManager(DataManagerInterface):
    """
    A data manager class that handles SQLite database interactions 
    for users and movies.
    """

    def __init__(self, db_file_name):
        """
        Initialize the SQLiteDataManager with a SQLite database file.

        Args:
            db_file_name (str): The name of the SQLite database file.
        """
        self.engine = create_engine(f'sqlite:///{db_file_name}')
        self.Session = sessionmaker(bind=self.engine)
        db.metadata.create_all(self.engine)


    # Retrieves all users from the database
    def get_all_users(self):
        """
        Retrieve all users from the database.

        Returns:
            list: A list of User objects.
        """
        session = self.Session()
        stmt = select(User)
        result = session.execute(stmt).scalars().all()
        session.close()
        return result


    # Retrieves all movies for a given user from the database
    def get_user_movies(self, user_id):
        """
        Retrieve all movies associated with a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of Movie objects associated with the given user.
        """
        session = self.Session()
        stmt = select(Movie).where(Movie.user_id == user_id)
        result = session.execute(stmt).scalars().all()
        session.close()
        return result


    # Adds a new user to the database
    def add_user(self, user_id, name):
        """
        Add a new user to the database.

        Args:
            user_id (str): The unique ID of the user.
            name (str): The name of the user.

        Returns:
            None
        """
        session = self.Session()
        new_user = User(id=user_id, name=name)
        session.add(new_user)
        session.commit()
        session.close()


    # Adds a new movie to the database
    def add_movie(self, movie_id, name):
        """
        Add a new movie to the database.

        Args:
            movie_id (int): The unique ID of the movie.
            name (str): The name of the movie.

        Returns:
            None
        """
        session = self.Session()
        new_movie = Movie(id=movie_id, name=name)
        session.add(new_movie)
        session.commit()
        session.close()


    # Updates details of a movie in the database
    def update_movie(self, movie_id, name=None, director=None, year=None, rating=None):
        """
        Update details of an existing movie in the database.

        Args:
            movie_id (int): The ID of the movie to be updated.
            name (str, optional): The new name of the movie.
            director (str, optional): The new director of the movie.
            year (int, optional): The new release year of the movie.
            rating (float, optional): The new rating of the movie.

        Returns:
            None
        """
        session = self.Session()
        movie = session.query(Movie).filter(Movie.id == movie_id).one_or_none()

        if movie:
            if name is not None:
                movie.name = name
            if director is not None:
                movie.director = director
            if year is not None:
                movie.year = year
            if rating is not None:
                movie.rating = rating

            session.commit()
        else:
            print("Movie not found.")

        session.close()


    # Deletes a movie from the database
    def delete_movie(self, movie_id):
        """
        Delete a movie from the database.

        Args:
            movie_id (int): The ID of the movie to be deleted.

        Returns:
            None
        """
        session = self.Session()
        movie = session.query(Movie).filter(Movie.id == movie_id).first()

        if movie:
            session.delete(movie)
            session.commit()
        else:
            print("Movie not found.")

        session.close()
