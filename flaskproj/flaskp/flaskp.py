import os
import sqlite3
from login_check import checkname, getaccounts
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db')))
app.config.update(dict(SECRET_KEY='dev key'))
app.config.from_envvar('FLASKHACK_SETTINGS', silent=True)

def connect_db():
	"""Connects to the specific database."""
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv
def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db
@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()
def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode = 'r') as f:
		db.cursor().executescript(f.read())
	db.commit()
@app.cli.command('initdb')
def initdb_command():
	init_db()
	print('Initialized the database.')

@app.route('/')
def start():
	return render_template('login.html')
@app.route('/login', methods = ['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		num = request.form['aid']
		first = request.form['first']
		last = request.form['last']
		zipp = request.form['zip']
		if checkname(num,first,last,zipp)[0]==1:
			session['first'] = first
			session['num'] = num
			session['last'] = last
			session['zip'] = zipp
			return redirect(url_for('show_landing'))
		else:
			error = checkname(num,first,last,zipp)[1]
			return render_template('login.html', error=error)
	else :
		return render_template('login.html', error=error)

@app.route('/landing')
def show_landing():
	checking = filter(lambda x: x[3] == 'checking', getaccounts(session['num']))
	saving=filter(lambda x: x[3] == 'saving', getaccounts(session['num']))
	credit=filter(lambda x: x[3] == 'credit', getaccounts(session['num']))
	db = get_db()
	actions = db.execute('select action from actions')
	actlist = actions.fetchall()
	#print (actlist)
	params = []
	for x in actlist:
		params.append(db.execute('select actionName, paramName from params where actionName = (?)', x).fetchall())
	#print params
	return render_template('landing.html', checking = checking, saving = saving, credit = credit, actlist = actlist, paramStruct = params)

