from typing import cast

from flask_sqlalchemy import SQLAlchemy  # Wenn du Flask verwendest, ansonsten direkt von sqlalchemy importieren.
from sqlalchemy.orm import sessionmaker  # ORM-Funktionen aus dem richtigen Modul importieren
from sqlalchemy import create_engine, select  # Entferne `create`, das gibt es nicht als separates Modul.
from datamanager.data_manager_interface import DataManagerInterface

db = SQLAlchemy()
print(db)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    director = db.Column(db.String)
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    user_id = db.Column(db.Integer)

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.engine = create_engine(f'sqlite:///{db_file_name}')#create a connection to database using the file name
        
        # Initialize a session maker that will be used to create sessions for database interactions
        self.Session = sessionmaker(bind=self.engine)
        db.metadata.create_all(self.engine) #create all tables in the database for user and movie


    def get_all_users(self):
        session = self.Session()  #opens session
        stmt = select(User)  #SQLAlchemy-Statement for select
        result = session.execute(stmt).scalars().all()  #execute and show result
        session.close()  #closes session
        return result

    def get_user_movies(self, user_id):
        session = self.Session()  # Erstelle eine neue Sitzung
        stmt = select(Movie).where(cast("ColumnElement[bool]",Movie.user_id == user_id))  # Beispiel für JOIN und WHERE-Klausel
        result = session.execute(stmt).scalars().all()  # Führe die Abfrage aus und erhalte alle Ergebnisse
        session.close()  # Schließe die Sitzung
        return result  # Gibt die Ergebnisse zurück

    def add_user(self, user_id, name):
        session = self.Session()
        new_user = User(id=user_id, name=name) #creates a new user
        session.add(new_user) #insert new user obj. to session
        session.commit() #confirms the session and saves it
        session.close()
    
    def add_movie(self, movie_id, name):
        session = self.Session()
        new_movie = Movie(id=movie_id, name=name)
        session.add(new_movie)
        session.commit()
        session.close()

    def update_movie(self, movie_id, name=None, director=None, year=None, rating=None):
        session = self.Session() 
        
        #find movie through movie_id
        movie = session.query(Movie).filter(Movie.id == movie_id).one_or_none()
        
        if movie:
            # update Details of movies, if values where given
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

    def delete_movie(self, movie_id):
        session = self.Session()
        movie = session.query(Movie).filter(Movie.id == movie_id).first

        if movie:
            session.delete(movie)
            session.commit()
        else:
            print("Movie not found.")   
            
        session.close()

