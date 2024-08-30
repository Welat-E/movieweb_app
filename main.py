#from Flask import flask
from datamanager.data_manager_interface import DataManagerInterface


class Datamanager:
    def __init__(self):
        self.users = {}
        self.movies = {}

    def add_user(self, user_id, name):
        """Adds a new user"""
        if user_id not in self.users:
             self.users[user_id] = {'name': name}
        else:
             print("User exists already.")

    
    def add_movie(self, movie_id, name, director, year, rating):
        """Adds a new movie."""
        if movie_id not in self.movies:
            self.movies[movie_id] = {'name': name, 'director': director, 'year': year, 'rating': rating}
        else:
            print("Movie already exists.")


    def update_movie(self, movie_id, name=None, director=None, year=None, rating=None):
        """Updates details of a movie."""
        if movie_id in self.movies:
            if name is not None:
                self.movies[movie_id]['name'] = name
            if director is not None:
                self.movies[movie_id]['director'] = director
            if year is not None:
                self.movies[movie_id]['year'] = year
            if rating is not None:
                self.movies[movie_id]['rating'] = rating

        else:
            print("Movies doesn't exist.")


    def delete_movie(self, movie_id):
        """Deltes movies from storage."""
        if movie_id in self.movies:
            del self.movies['movie_id']
        else:
            print("Movie not found.")


    def get_user(self, user_id):
        """Gives informations about a user."""
        return self.users.get(user_id)
    

    def get_moives(self, movie_id):
        """Gives informations about a movie."""
        return self.movies.get(movie_id)
    

