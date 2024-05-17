from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key
app.config['DATABASE'] = 'hackathon_registration.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        team_name = request.form['team_name']
        email = request.form['email']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()

        db = get_db()
        cursor = db.cursor()

        # Check if the email is already registered
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        data = cursor.fetchone()

        if data:
            return "Email already registered. Please use a different email."

        # Insert new user into the database
        cursor.execute("INSERT INTO users (name, team_name, email, password) VALUES (?, ?, ?, ?)",
                       (name, team_name, email, password))

        db.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()

        db = get_db()
        cursor = db.cursor()

        # Check if the email and password match
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        data = cursor.fetchone()

        if data:
            session['email'] = email
            return "Login successful!"
        else:
            return "Incorrect email or password. Please try again."

    return render_template('login.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
