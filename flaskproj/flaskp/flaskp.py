import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file
app.config.from_envvar('FLASKHACK_SETTINGS', silent=True)
@app.route('/login', methods = ['GET', 'POST'])
	if request.method == 'POST':
		first = request.form['first']
		num = request.form['aid']
		last = request.form['last']
		zip = request.form['zip']
		if checkname(num,first,last,zip)[0]==1:
			session['first'] = first
			session['num'] = num
			session['last'] = last
			session['zip'] = zip
			return redirect(url_for('landing')
		else:
			return(login.html, error = checkname(num,first,last,zip)[1])

@app.route('/landing')
def show_landing():
	checking = filter(lambda x: x = 'checking', getaccounts(session['num'])
	saving=filter(lambda x: x = 'saving', getaccounts(session['num'])
	credit=filter(lambda x: x = 'credit', getaccounts(session['num'])
	return render_template('landing.html', checking = checking, saving = saving, credit = credit)

			
