#!/usr/bin/python3
from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)
app.secret_key='your_secret_key'   #Required for sessions

# Hardcoded credentials for the example
USER_DATA = {"admin" : "password123"}

@app.route('/')
def home():
    if 'username' in session:
        return f'logged in as {session["username"]} | <a href="/logout>Logout<a/>"'

    return 'You are not logged in | <a href="/login">Login</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        #Check credentials
        if username in USER_DATA and USER_DATA[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        
        else:
            return 'Wrong Username/password!Check please'

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

