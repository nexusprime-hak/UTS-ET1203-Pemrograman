from flask import render_template, Flask, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, logout_user, LoginManager, UserMixin
from satellite_parser import parse_satellite_data
from werkzeug.security import generate_password_hash, check_password_hash
import re
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_pengguna.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<user {self.username}>'

# Create database tables
with app.app_context():
    db.create_all()

with open('data/infoboard.json', 'r') as file:
    infoboard = json.load(file)

@app.route('/')
def index():
    # Redirect to login if no session, else go to the homepage
    if 'user_ud' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('entrypage'))

def email_validate(email):
    email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

@app.route('/home', methods=["GET","POST"])
def entrypage():
    # display map widget
    if 'user_ud' not in session:
        flash('Please log in to access the homepage.', 'error')
        return redirect(url_for('login'))
    else:
        satellites_data = infoboard
        satellite_names = [sat["name"] for sat in satellites_data]
        norad_n2yo = parse_satellite_data()

        # Additional fixed values for other variables
        size_n2yo = 'medium'
        allpasses_n2yo = '0'
        map_n2yo = '5'

        return render_template('entrypage.html', 
                               norad_n2yo=norad_n2yo, 
                               size_n2yo=size_n2yo,
                               allpasses_n2yo=allpasses_n2yo,
                               map_n2yo=map_n2yo,
                               satellites=satellite_names
                               )

@app.route("/get_satellite_info", methods=["POST"])
@login_required
def get_satellite_info():
    selected_name = request.json.get("satellite")
    if not selected_name:
        return jsonify({"error": "No satellite selected"}), 400
    satellites_data = infoboard
    selected_satellite = next(
        (sat for sat in satellites_data if sat["name"] == selected_name), None
    )
    return jsonify(selected_satellite)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        print(request.form)
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Password validation
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))
        elif not email_validate(email):
            flash("Invalid email format!")
            return redirect(url_for('register'))
        else:
            # Check if username or email already exists
            existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
            if existing_user:
                flash('Username or email already exists!', 'error')
                return redirect(url_for('register'))

            # Hash the password with a valid method
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            # Save new user to the database
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            # Log the user after registration
            login_user(new_user, remember=True)

            # Set the user in session
            session['user_ud'] = new_user.id

            flash('Account created successfully! You are now logged in.', 'success')
            return redirect(url_for('entrypage'))
    
    return render_template('register.html')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Check if user exists
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password!', 'error')
            return redirect(url_for('login'))

        login_user(user, remember=True)
        flash(f'Welcome, {username}!', 'success')
        return redirect(url_for('entrypage'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out succesfully", 'info')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)