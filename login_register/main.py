from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Add logic to validate user login here
    return f"Welcome back, {username}!"

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    if password != confirm_password:
        return "Passwords do not match!", 400
    
    # Add logic to register the user here
    return f"Account created for {username} with email {email}!"

if __name__ == '__main__':
    app.run(debug=True)
