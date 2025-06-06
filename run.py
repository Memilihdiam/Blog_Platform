from flask import Flask, render_template, request, url_for, redirect, session
from pymongo import MongoClient
from werkzeug.security import check_password_hash
from datetime import datetime

app = Flask(__name__, template_folder='app/templates')
app.secret_key = 'your-secret-key-here'
Port = 5130

client = MongoClient('mongodb://localhost:27017')
db = client['blog_platform']
users = db['users']
post = db['posts']
komen = db['comments']
like = db['likes']
kategori = db['categories']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = users.find_one({'username': username})
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['username'] = username
            return redirect(url_for('main_menu'))
        else:
            return render_template('index.html', error='Invalid username or password')
    
    return render_template('index.html')

@app.route('/add')
def register():
    if request.method == "POST":
        user = {
            "username": request.form['username'],
            "email": request.form['email'],
            "password": request.form['password'], 
            "created_at": datetime.utcnow(),
            "update_at": datetime.utcnow()
        }
    users.insert_one(user)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=False, port=Port)
