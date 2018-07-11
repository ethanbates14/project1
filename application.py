import os

from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
from flask_session import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import requests,json

app = Flask(__name__)

# Check for DB environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#routing
@app.route("/", methods=['GET', 'POST'])
def index():
	""" Session """
	if not session.get('logged_in'):
		return render_template('index.html')
	else:
		return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Login Form"""
	if request.method == 'GET':
		return render_template('login.html')
	else:
		uname = request.form['username']
		passw = request.form['password']
		try:
			userdata = db.execute("SELECT * FORM p1_users WHERE username = :x AND usr_pwd = :y", {"x": uname, "y": passw}).fetchone()

			if userdata is not None:
				session['logged_in'] = True
				return redirect(url_for('search'))
			else:
				return render_template('error.html', message='Invalid Login')
		except:
			return render_template('error.html', message='Invalid Login')

@app.route('/register/', methods=['GET', 'POST'])
def register():
	"""Register Form"""
	if request.method == 'GET':
		return render_template('register.html')
	else:
		first_name=request.form['firstname']
		last_name=request.form['lastname']
		username=request.form['username']
		usr_pwd=request.form['password']

		#Logic to check if user already exists
		check_data = db.execute("SELECT * FROM p1_users WHERE username = :x", {"x": username}).fetchall()

		if check_data is not None:
			return render_template('error.html', message='User Already Exists!')
		else:
			db.execute("INSERT INTO p1_users (first_name, last_name, username, usr_pwd) VALUES (:a, :b, :c, :d)",
				{"a": first_name, "b": last_name, "c": username, "d": usr_pwd })
		db.commit()
		return render_template('login.html')
	return render_template('register.html')

@app.route("/logout")
def logout():
	"""Logout Form"""
	session['logged_in'] = False
	return redirect(url_for('index'))


@app.route("/search", methods=['GET', 'POST'])
def search():
	"""Search Form"""
	if request.method == "GET":
		return render_template("search.html")
	else:
		return render_template("results.html")


@app.route("/results", methods=['POST'])
def results():
	search_param = request.form['search_param']
	search_val = request.form['param_val']

	if search_param == 'zipcode':
		loc_data = db.execute("SELECT * FROM p1_cities WHERE zipcode like %:x%", {"x": search_val}).fetchall()
	elif search_param == 'cityname':
		search_val = search_val.upper()
		loc_data = db.execute("SELECT * FROM p1_cities WHERE city_name like %:x%", {"x": search_val}).fetchall()

	return render_template("results.html", locations=loc_data)

@app.route("/location")
def location():
	ds_apikey="9a80dd9e0d1a1d0ca8931b3899507105"
	weather = requests.get("https://api.darksky.net/forecast/9a80dd9e0d1a1d0ca8931b3899507105/42.37,-71.11").json()
	return render_template("location.html",weather=weather)

@app.route("/api/<string:zipcode>")
def zipcode_api(zipcode):
    """API Data From ZipCode"""

    # Make sure zipcode exists.
    api_data = db.execute("SELECT * FROM p1_cities WHERE zipcode = :x", {"x": zipcode}).fetchall()
    if api_data is None:
        return jsonify({"error": "Invalid ZIP CODE"}), 422

    # Get all passengers.
    return jsonify({
            "zipcode": api_data.city_name,
            "cityname": api_data.zipcode,
            "duration": api_data.state_id
        })

if __name__ == '__main__':
    app.run(debug=True)