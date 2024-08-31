#from crypt import methods
from flask import Flask, request, render_template, url_for, flash, redirect
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


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_id = request.form['user_id']
        name = request.form['name']
    else:
        return render_template()
    return redirect(url_for('/'))





#delete movie muss man POST method verwenden

if __name__ == '__main__':
    app.run(debug=True)