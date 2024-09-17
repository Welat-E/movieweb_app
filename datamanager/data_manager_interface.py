
# Abstract base class defining data manager methods
from abc import ABC, abstractmethod
import json


class DataManagerInterface(ABC):
    """
    Abstract base class to declare the required methods
    for any data manager class that interacts with user and movie data.
    """

    @abstractmethod
    def get_all_users(self):
        """
        Retrieve all users.

        This method must be implemented by any subclass of DataManagerInterface.

        Returns:
            list: A list of user details.
        """
        pass


    @abstractmethod
    def get_user_movies(self, user_id):
        """
        Retrieve all movies associated with a specific user.

        Args:
            user_id (int): Unique identifier for the user.

        Returns:
            list: A list of movies for the given user.
        """
        pass


# JSON-based implementation of DataManagerInterface
class JSONDataManager(DataManagerInterface):
    """
    A data manager class that manages users and movies using JSON format.
    This class implements the methods defined in DataManagerInterface.
    """

    def __init__(self):
        """
        Initialize the JSONDataManager with users and movies dictionaries.
        """
        self.users = {}
        self.movies = {}


    # Retrieves all users from the system
    def get_all_users(self):
        """
        Retrieve a list of all users.

        Returns:
            list: A list of all users stored in the system.
        """
        return list(self.users.values())


    # Retrieves all movies for a given user
    def get_user_movies(self, user_id):
        """
        Retrieve all movies associated with a specific user.

        Args:
            user_id (int): Unique identifier for the user.

        Returns:
            list: A list of movies for the given user, or an empty list if the user has no movies.
        """
        return self.movies.get(user_id, [])


    # Saves users and movies data to a JSON file
    def save_to_json(self, file_path):
        """
        Save the users and movies data to a JSON file.

        Args:
            file_path (str): The path to the file where data should be saved.

        Returns:
            None
        """
        data = {
            'users': self.users,
            'movies': self.movies
        }
        with open(file_path, 'w') as f:
            json.dump(data, f)


    # Loads users and movies data from a JSON file
    def load_from_json(self, file_path):
        """
        Load the users and movies data from a JSON file.

        Args:
            file_path (str): The path to the file from which data should be loaded.

        Returns:
            None
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
            self.users = data.get('users', {})
            self.movies = data.get('movies', {})
