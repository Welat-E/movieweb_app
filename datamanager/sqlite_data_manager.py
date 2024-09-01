from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from datamanager.data_manager_interface import DataManagerInterface

db = SQLAlchemy()


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
        self.engine = create_engine(f'sqlite:///{db_file_name}')
        self.Session = sessionmaker(bind=self.engine)
        db.metadata.create_all(self.engine)

    def get_all_users(self):
        session = self.Session()
        stmt = select(User)
        result = session.execute(stmt).scalars().all()
        session.close()
        return result

    def get_user_movies(self, user_id):
        session = self.Session()
        stmt = select(Movie).where(Movie.user_id == user_id)
        result = session.execute(stmt).scalars().all()
        session.close()
        return result

    def add_user(self, user_id, name):
        session = self.Session()
        new_user = User(id=user_id, name=name)
        session.add(new_user)
        session.commit()
        session.close()

    def add_movie(self, movie_id, name):
        session = self.Session()
        new_movie = Movie(id=movie_id, name=name)
        session.add(new_movie)
        session.commit()
        session.close()

    def update_movie(self, movie_id, name=None, director=None, year=None, rating=None):
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

    def delete_movie(self, movie_id):
        session = self.Session()
        movie = session.query(Movie).filter(Movie.id == movie_id).first()

        if movie:
            session.delete(movie)
            session.commit()
        else:
            print("Movie not found.")

        session.close()
