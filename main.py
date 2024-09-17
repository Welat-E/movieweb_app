# Datamanager class handling users and movies data
from datamanager.data_manager_interface import DataManagerInterface


class Datamanager:
    """Initialize the Datamanager with users and movies dictionaries."""

    def __init__(self):
        self.users = {}
        self.movies = {}

    # Adds a new user to the system
    def add_user(self, user_id, name):
        """
        Adds a new user to the user dictionary.

        Args:
            user_id (int): Unique identifier for the user.
            name (str): Name of the user.

        Returns:
            None
        """
        if user_id not in self.users:
            self.users[user_id] = {"name": name}
        else:
            print("User exists already.")

    # Adds a new movie to the system
    def add_movie(self, movie_id, name, director, year, rating):
        """
        Adds a new movie to the movies dictionary.

        Args:
            movie_id (int): Unique identifier for the movie.
            name (str): Title of the movie.
            director (str): Director of the movie.
            year (int): Year the movie was released.
            rating (float): Movie's rating.

        Returns:
            None
        """
        if movie_id not in self.movies:
            self.movies[movie_id] = {
                "name": name,
                "director": director,
                "year": year,
                "rating": rating,
            }
        else:
            print("Movie already exists.")

    # Updates the details of an existing movie
    def update_movie(self, movie_id, name=None, director=None, year=None, rating=None):
        """
        Updates details of an existing movie. If a parameter is not provided, it remains unchanged.

        Args:
            movie_id (int): Unique identifier for the movie.
            name (str, optional): New title for the movie. Defaults to None.
            director (str, optional): New director name. Defaults to None.
            year (int, optional): New release year. Defaults to None.
            rating (float, optional): New movie rating. Defaults to None.

        Returns:
            None
        """
        if movie_id in self.movies:
            if name is not None:
                self.movies[movie_id]["name"] = name
            if director is not None:
                self.movies[movie_id]["director"] = director
            if year is not None:
                self.movies[movie_id]["year"] = year
            if rating is not None:
                self.movies[movie_id]["rating"] = rating
        else:
            print("Movie doesn't exist.")

    # Deletes a movie from the system
    def delete_movie(self, movie_id):
        """
        Deletes a movie from the movies dictionary.

        Args:
            movie_id (int): Unique identifier for the movie to be deleted.

        Returns:
            None
        """
        if movie_id in self.movies:
            del self.movies[movie_id]
        else:
            print("Movie not found.")

    # Retrieves user information
    def get_user(self, user_id):
        """
        Retrieves user information from the user dictionary.

        Args:
            user_id (int): Unique identifier for the user.

        Returns:
            dict: User information if found, otherwise None.
        """
        return self.users.get(user_id)

    # Retrieves movie information
    def get_movies(self, movie_id):
        """
        Retrieves movie information from the movies dictionary.

        Args:
            movie_id (int): Unique identifier for the movie.

        Returns:
            dict: Movie information if found, otherwise None.
        """
        return self.movies.get(movie_id)
