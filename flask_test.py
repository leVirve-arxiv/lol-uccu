from flask import Flask
from flask import render_template, request, redirect, url_for

from Summoner import *

app = Flask(__name__)

@app.route('/')
def index():
    online_users = 1 # mongo.db.users.find({'online': True}).count()
    print('online: ', online_users)
    return render_template('index.html',
            online_users=online_users)

@app.route('/summoner/<username>')
def show_user_profile(username):
    return query(username)

@app.route('/summoner/', methods=['GET', 'POST'])
def action_form():
    if request.method == 'POST':
        username = request.form['query_name']
        return redirect(url_for('show_user_profile', username=username))
    else:
        return render_template('form.html')

@app.errorhandler(404)
def page_not_found(error):
        return render_template('page_not_found.html'), 404

def query(name):
    s = Summoner(name)
    games = s.get_recent_games()
    return render_template('user.html',
            username=name, games=games)

if __name__ == '__main__':
    app.run(debug=True)

