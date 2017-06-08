import os
import sqlite3
from login_check import checkname, getaccounts, getdeposits
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response
import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

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
	session['flag'] = ""
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
			session['flag']=True
			return redirect(url_for('show_landing'))
		else:
			error = checkname(num,first,last,zipp)[1]
			return render_template('login.html', error=error)
	else :
		return render_template('login.html', error=error)

@app.route('/landing')
def show_landing():
	checking = filter(lambda x: x[3] == 'Checking', getaccounts(session['num']))
	saving=filter(lambda x: x[3] == 'Savings', getaccounts(session['num']))
	credit=filter(lambda x: x[3] == 'Credit Card', getaccounts(session['num']))
	db = get_db()
	actions = db.execute('select action from actions')

	actlist = actions.fetchall()
	print checking
	print actlist
	params = []
	for x in actlist:
		params.append(db.execute('select actionName, paramName from params where actionName = (?)', x).fetchall())
	#print params
	return render_template('landing.html', checking = checking, saving = saving, credit = credit, actlist = actlist, paramStruct = params)
@app.route('/select')
def select():
	if request.form["Show deposits"]:
		session['flag'] = "Show deposits"
		return redirect(url_for('show_landing'))
	elif request.form["Show withdrawals"]:
		session['flag'] = "Show withdrawals"
		return redirect(url_for('show_landing'))
	elif request.form["Show all transactions"]:
		session['flag'] = "Show all transactions"
		return redirect(url_for('show_landing'))
	elif request.form["Average inflow"]:
		session['flag'] = "Average inflow"
		return redirect(url_for('show_landing'))
	elif request.form["Average outflow"]:
		session['flag'] = "Average outflow"
		return redirect(url_for('show_landing'))
	elif request.form["Daily average inflow"]:
		session['flag'] = "Daily average inflow"
		return redirect(url_for('show_landing'))
	elif request.form["Daily average outflow"]:
		session['flag'] = "Daily average outflow"
		return redirect(url_for('show_landing'))
	elif request.form["Daily average net"]:
		session['flag'] = "Daily average net"
		return redirect(url_for('show_landing'))
@app.route('/compute', methods = ['POST'])
def compute():
<<<<<<< HEAD
		if request.method == 'POST':
			session['flag']=True
			acctlist=[]
			for x in getaccounts(session['num']):
				if request.form[x[0]]==0:
					acctlist.append[x[0]]
			if request.form["Show deposits"]:
				retList = []
				for x in acctlist:
					retList.append(getdeposits(x))
				session['data'] = retList
				redirect(url_for('show_landing'))
			elif request.form["Show withdrawals"]:
				retList = []
				for x in acctlist:
					retList.append(getwithdrawals(x))
				session['data'] = retList
				redirect(url_for('show_landing'))
			elif request.form["Show all transactions"]:
				retList = []
				for x in acctlist:
					retList.append(getdeposits(x))
					retList.append(getwithdrawals(x))
				session['data'] = retList
				redirect(url_for('show_landing'))
=======
	if request.method == 'POST':
		session['flag']=True
		acctlist=[]
		for x in getaccounts(session['num']):
			if request.form[x[0]]==0:
				acctlist.append[x[0]]

		depositlist = []
		withdrawallist = []
		for accountid in acctlist:
			depositlist += getdeposits(accountid)
			withdrawallist += getwithdrawals(accountid)

		if request.form["Show deposits"]:
			retList = []
			for x in acctlist:
				retList.append(getdeposits(x))
			session['data'] = retList
			redirect(url_for('show_landing'))
		elif request.form["Show withdrawals"]:
			retList = []
			for x in acctlist:
				retList.append(getwithdrawals(x))
			session['data'] = retList
			redirect(url_for('show_landing'))
		elif request.form["Show all transactions"]:
			retList = []
			for x in acctlist:
				retList.append(getdeposits(x))
				retList.append(getwithdrawals(x))
			session['data'] = retList
			redirect(url_for('show_landing'))
		elif request.form["Average inflow"]:
			fig = plot_cashflow(depositlist, None, request.form[x[1]], 1, 1)
			canvas = FigureCanvas(fig)
    		output = StringIO.StringIO()
    		canvas.print_png(output)
    		response = make_response(output.getvalue())
    		response.mimetype = 'image/png'
    		session['data'] = response

			redirect(url_for('show_landing'))
>>>>>>> b8855db4ca4a677d3d79d56d7c13170b5117601d
