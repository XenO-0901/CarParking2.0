from flask import Flask, render_template, session, request, g, redirect, url_for
import os
import sqlite3

#if you want to use the save info in the database the url must be http://localhost:5001/login

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL, phone TEXT NOT NULL, platenumber TEXT NOT NULL)')
        db.commit()
    return db


@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']

@app.route('/')
def index():
    return render_template('loading.html')

@app.route('/userview')
def userview():
    if g.user:
        return render_template('index.html', user=session['user'])
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cur = db.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cur.fetchone()

        if user:
            session['user'] = user['username']
            return redirect(url_for('userview'))
        else:
            return render_template('login.html', error='Invalid username or password')

    # Handle GET requests
    return render_template('login.html')


@app.route('/forgotpass', methods={'GET', 'POST'})
def forgotpass():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    #cur = db.execute('SELECT * FROM users WHERE username = ?', (username))
    cur = db.execute('UPDATE users SET password = ? WHERE username = ?', (password, username))
    db.commit()

    if cur.rowcount > 0:
        session['user'] = username
        return redirect(url_for('userview'))
    else:
        return render_template('forgotpass.html', error='Invalid password')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['name']
        platenumber = request.form['platenumber']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        db = get_db()

        try:
            db.execute('INSERT INTO users (username, platenumber, email, phone, password) VALUES (?, ?, ?, ?, ?)', (username, platenumber, email, phone, password))
            db.commit()
            session['user'] = username
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('signup.html', error='Username already exists')

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(port=5001)
