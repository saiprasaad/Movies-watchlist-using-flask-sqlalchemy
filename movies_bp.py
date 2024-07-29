from flask import Blueprint, flash, request, session, render_template, redirect, url_for
from models import db, User, Movie, MovieWatchList
import requests

movies_bp = Blueprint('movies', __name__)

@movies_bp.route("/")
def home():
    if 'user' not in session or 'userid' not in session:
        flash('Login first to continue')
        return redirect(url_for('movies.login'))
    return render_template('home.html')

@movies_bp.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Missing required fields')
            return render_template('login.html') 
        user = User.query.filter_by(username=username).first()
        if not user or user.password != password:
            flash('Incorrect login credentials')
            return render_template('login.html') 
        session['user'] = user.username
        session['userid'] = user.id
        return redirect(url_for('movies.home'))

@movies_bp.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Missing required fields')
            return render_template('register.html') 
        u = User(username=username, password=password)
        db.session.add(u)
        db.session.commit()
        flash('Registration Successful')
        return redirect(url_for('movies.login'))

@movies_bp.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('userid', None)
    session.pop('query', None)
    return redirect(url_for('movies.login')) 

@movies_bp.route("/results", methods = ['GET', "POST"])
def search_results():
    if 'user' not in session or 'userid' not in session:
        flash('Login first to continue')
        return redirect(url_for('movies.login'))
    if 'search' in request.form and len(request.form['search']) != 0:
        query = request.form['search']
        session['query'] = query
    elif 'query' in session:
        query = session['query']
    else:
        return render_template('home.html', error='Enter text to search')
        
    response = requests.get(f'https://www.omdbapi.com/?s={query}&apikey=51bb5fa5')
    response = response.json()
    movies = []
    for data in response['Search']:
        m = Movie(imdbID = data['imdbID'], title=data['Title'], year=data['Year'], type=data['Type'], poster=data['Poster'])
        movies.append(m)
    imdbIDS = MovieWatchList.query.with_entities(MovieWatchList.imdbID).filter_by(userid=session['userid']).all()
    imdbIDSList = [id[0] for id in imdbIDS]
    print(imdbIDSList)
    return render_template('movie_list.html', movies = movies, watchlist = imdbIDSList)

@movies_bp.route('/add-to-watchlist/<imdbID>', methods = ['POST'])
def add_to_watchlist(imdbID):
    if not imdbID:
        return render_template('movie_list.html')
    response = requests.get(f'https://www.omdbapi.com/?i={imdbID}&apikey=51bb5fa5')
    response = response.json()
    m = MovieWatchList(imdbID = response['imdbID'], title=response['Title'], year=response['Year'], type=response['Type'], poster=response['Poster'], userid=session['userid'])
    db.session.add(m)
    db.session.commit()
    return redirect(url_for('movies.search_results'))

@movies_bp.route('/remove-from-watchlist/<imdbID>', methods = ['POST'])
def remove_from_watchlist(imdbID):
    if not imdbID:
        return render_template('movie_list.html')
    MovieWatchList.query.filter_by(imdbID=imdbID).delete()
    db.session.commit()
    return redirect(url_for('movies.search_results'))

@movies_bp.route('/watchlists')
def watchlists():
    if 'user' not in session or 'userid' not in session:
        flash('Login first to continue')
        return redirect(url_for('movies.login'))
    movies = MovieWatchList.query.filter_by(userid=session['userid']).all()
    return render_template('watchlists.html', movies = movies)
    

