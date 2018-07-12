import os

from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
from flask_session import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import requests,json
import datetime

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
@app.route("/", methods=['GET'])
def index():
	""" Landing """
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
			userdata = db.execute("SELECT * FROM p1_users WHERE username = :x AND usr_pwd = :y", {"x": uname, "y": passw}).fetchone()

			if userdata is not None:
				session['user_id'] = uname
				session['logged_in'] = True
				session['first_name'] = userdata.first_name
				session['last_name'] = userdata.first_name
				session['user_no'] = userdata.id
				return redirect(url_for('search'))
			else:
				return render_template('error.html', message='Invalid Login')
		except:
			return render_template('error.html', message='Something went wrong')

@app.route('/register/', methods=['GET', 'POST'])
def register():
	"""Register Form"""
	if request.method == 'GET':
		return render_template('register.html')
	else:
		first_name=request.form['firstname']
		last_name=request.form['lastname']
		reg_username=request.form['username']
		usr_pwd=request.form['password']

		#Logic to check if user already exists
		check_data = db.execute("SELECT * FROM p1_users WHERE username = :x", {"x": reg_username}).fetchone()

		if check_data is not None:
			return render_template('error.html', message='User Already Exists!')
		else:
			db.execute("INSERT INTO p1_users (first_name, last_name, username, usr_pwd) VALUES (:a, :b, :c, :d)",
				{"a": first_name, "b": last_name, "c": reg_username, "d": usr_pwd })
		db.commit()
		return render_template('login.html')

@app.route("/logout")
def logout():
	"""Logout Form"""
	if session:
		session.clear()
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

	#Fuzzy Search and Case Sensitive
	search_val = "%" + search_val.upper() + "%"

	if search_param == 'zipcode':
		res_data = db.execute("SELECT * FROM p1_cities JOIN p1_states ON p1_states.id = p1_cities.state_id WHERE zipcode like :x",
			{"x": search_val}).fetchall()
	elif search_param == 'cityname':
		search_val = search_val.upper()
		res_data = db.execute("SELECT * FROM p1_cities JOIN p1_states ON p1_states.id = p1_cities.state_id WHERE city_name like :x",
			{"x": search_val}).fetchall()

	return render_template("results.html", locations=res_data, user_input=search_val,user_select=search_param)

@app.route("/location/<zipcode>", methods=['GET', 'POST'])
def location(zipcode):
	"""Location Data"""
	ds_apikey="9a80dd9e0d1a1d0ca8931b3899507105"
	sql_query = """
	SELECT
	a.city_name as place_name,b.state_abbrev as state,
	a.latitude as latitude,a.longitude as longitude,
	a.zipcode as zip,a.population as population,
	COUNT(c.id) as check_ins
	FROM p1_cities a
	JOIN p1_states b ON a.state_id = b.id
	LEFT JOIN p1_user_checkin c ON c.city_id = a.id
	WHERE a.zipcode = :x
	GROUP BY a.city_name,b.state_abbrev,
	a.latitude,a.longitude,a.zipcode,a.population
	"""

	# Make sure zipcode exists.
	loc_data = db.execute(f"{sql_query}", {"x": zipcode}).fetchall()
	if not loc_data:
		return render_template('error.html', message='Something went wrong')
	else:

		lat=str(loc_data[0][2])
		lng=str(loc_data[0][3])

		weather = requests.get(f"https://api.darksky.net/forecast/{ds_apikey}/{lat},{lng}").json()
		curr_weather = weather['currently']

		cw_time = datetime.datetime.fromtimestamp(curr_weather['time']).strftime('%Y-%m-%d %H:%M:%S')

		return render_template("location.html",curr_weather=curr_weather)

@app.route('/checkin', methods=['POST'])
def checkin():
	#city_id = request.form['city_id']
	comments=request.form['loc_comments']
	return f"{session['user_id']} | {comments}"

@app.route('/test', methods=['GET', 'POST'])
def test():
	return f"{session['user_no']} {session['logged_in']}"

@app.route("/api/<string:zipcode>", methods=['GET'])
def zipcode_api(zipcode):
    """API Data From ZipCode"""
    sql_query = """
    SELECT
    a.city_name as place_name,b.state_abbrev as state,
    a.latitude as latitude,a.longitude as longitude,
    a.zipcode as zip,a.population as population,
	COUNT(c.id) as check_ins
	FROM p1_cities a
	JOIN p1_states b ON a.state_id = b.id
	LEFT JOIN p1_user_checkin c ON c.city_id = a.id
	WHERE a.zipcode = :x
	GROUP BY a.city_name,b.state_abbrev,
	a.latitude,a.longitude,a.zipcode,a.population
    """

    # Make sure zipcode exists.
    api_data = db.execute(f"{sql_query}", {"x": zipcode}).fetchall()
    if not api_data:
        return jsonify({"error": "Invalid ZIP CODE"}), 422

    # Return JSON Data
    return jsonify({
            "place_name": str(api_data[0][0]),
            "state": str(api_data[0][1]),
            "latitude": str(api_data[0][2]),
            "longitude": str(api_data[0][3]),
            "zip": str(api_data[0][4]),
            "population": str(api_data[0][5]),
            "check_ins": str(api_data[0][6]),
        })

if __name__ == '__main__':
    app.run(debug=True)