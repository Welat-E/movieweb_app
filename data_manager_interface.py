from abc import ABC, abstractmethod
import json


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass


class JSONDataManager(DataManagerInterface):
    def __init__(self):
        self.users = {}
        self.movies = {}

    def get_all_users(self):
        return list(self.users.values())

    def get_user_movies(self, user_id):
        return self.movies.get(user_id, [])

    def save_to_json(self, file_path):
        data = {
            'users': self.users,
            'movies': self.movies
        }
        with open(file_path, 'w') as f:
            json.dump(data, f)

    def load_from_json(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            self.users = data.get('users', {})
            self.movies = data.get('movies', {})

#
