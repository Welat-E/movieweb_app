from flask import Flask
from datamanager.sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)
data_manager = SQLiteDataManager("data/users_movies.sqlite")

@app.route('/')
def home():
    return "Welcome to MovieWeb App!"





@app.route('/users', methods=['GET'])
def list_users():
  users = data_manager.get_all_users()
  return users

@app.route('/users/<int:user_id>')
def get_user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)
    return movies




#delete movie muss man POST method verwenden

if __name__ == '__main__':
    app.run(debug=True)