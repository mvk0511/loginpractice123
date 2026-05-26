from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

USERS_FILE = 'users.json'

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json

    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    with open(USERS_FILE, 'r') as f:
        users = json.load(f)

    users.append({
        'email': email,
        'username': username,
        'password': password
    })

    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    username = data.get('username')
    password = data.get('password')

    with open(USERS_FILE, 'r') as f:
        users = json.load(f)

    for user in users:
        if user['username'] == username and user['password'] == password:
            return jsonify({'message': 'Login successful'})

    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
