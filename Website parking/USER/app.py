from flask import Flask, render_template, session, request, g, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.pop('user', None)

        if request.form['password'] == 'password':
            session['user'] = request.form['username']
            return redirect(url_for('userview'))
        
    return render_template('LoginPage.html')

@app.route('/userview')
def userview():
    if g.user:
        return render_template('index.html', user=session['user'])
    return redirect(url_for('index'))

@app.route('/omg')
def omg():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle form submission
        name = request.form['name']
        platenumber = request.form['plateno']
        email = request.form['email']
        phone = request.form['contact']
        password = request.form['password']
        conpassword = request.form['conpassword']

        # Do something with the form data (e.g. save to database)

        return "Thanks for signing up, " + name + "!"

    # If the request method is GET, render the signup page
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(port=5001)
