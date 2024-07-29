from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    watchlists = db.relationship('MovieWatchList', backref = 'user', lazy = False)
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Movie():
    def __init__(self, imdbID, title, year, type, poster):
        self.imdbID = imdbID
        self.title = title
        self.year= year
        self.type = type
        self.poster = poster

class MovieWatchList(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    imdbID = db.Column(db.String(100))
    year = db.Column(db.String(100))
    title = db.Column(db.String(500))
    year = db.Column(db.String(100))
    poster = db.Column(db.String(1000))
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    def __init__(self, imdbID, title, year, type, poster, userid):
        self.imdbID = imdbID
        self.title = title
        self.year= year
        self.type = type
        self.poster = poster
        self.userid = userid