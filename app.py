from flask import Flask, request, render_template, url_for, redirect
from datamanager.sqlite_data_manager import SQLiteDataManager, User, db, Movie

app = Flask(__name__)

# Initialisiere SQLAlchemy mit der Flask-App
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/users_movies.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialisiere den Datenbankmanager
data_manager = SQLiteDataManager("data/users_movies.sqlite")

@app.route('/')
def home():
    return "Welcome to MovieWeb App!"

@app.route('/users', methods=['GET'])
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)  # Verwende das Template für die Benutzerliste

@app.route('/users/<int:user_id>')
def get_user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user_id=user_id, movies=movies)  # Verwende ein Template, um Filme anzuzeigen

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_id = request.form['user_id']
        name = request.form['name']
        record = User(id=user_id, name=name)
        db.session.add(record)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_user.html')

@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        title = request.form['name']
        movie = Movie(name=title, user_id=user_id)  # Füge den user_id hinzu
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('get_user_movies', user_id=user_id))
    return render_template('add_movie.html', user_id=user_id)

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        new_title = request.form['name']
        movie.name = new_title
        db.session.commit()
        return redirect(url_for('get_user_movies', user_id=user_id))

    return render_template('update_movie.html', user_id=user_id, movie=movie)

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('get_user_movies', user_id=user_id))

if __name__ == '__main__':
    app.run(debug=True)
