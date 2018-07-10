import os

from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_session import Session

from sqlalchemy import create_engine,Table,Column,Integer,Numeric,String,Date,ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

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
Base = declarative_base()

# Table Classes
class States(Base):
	__tablename__ = 'p1_states'
	id = Column(Integer, primary_key=True)
	state_abbrev = Column(String, nullable=False)
	def __repr__(self):
		return "<States(state_abbrev='%s')>" % (
			self.state_abbrev)

class Cities(Base):
	__tablename__ = 'p1_cities'
	id = Column(Integer, primary_key=True)
	city_name = Column(String, nullable=False)
	state_id = Column(Integer, ForeignKey('states.id'))
	zipcode = Column(String, nullable=False)
	latitude = Column(Numeric)
	longitude = Column(Numeric)
	population = Column(Integer)
	def __repr__(self):
		return "<Cities(city_name='%s', state_id='%s', zipcode='%s', latitude='%s',longitude='%s',population='%s',)>" % (
			self.city_name, self.state_id, self.zipcode, self.latitude, self.longitude,self.population)

class User(Base):
	__tablename__ = 'p1_users'
	id = Column(Integer, primary_key=True)
	first_name = Column(String)
	last_name = Column(String)
	username = Column(String)
	usr_pwd = Column(String)
	def __repr__(self):
		return "<User(first_name='%s', last_name='%s', username='%s', usr_pwd='%s',)>" % (
			self.last_name, self.last_name, self.username, self.usr_pwd)

class Checkin(Base):
	__tablename__ = 'p1_user_checkin'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'))
	city_id = Column(Integer, ForeignKey('cities.id'))
	check_in_date = Column(Date)
	usr_comments = Column(String)
	def __repr__(self):
		return "<Checkin(user_id='%s', city_id='%s', check_in_date='%s', usr_comments='%s',)>" % (
			self.user_id, self.city_id, self.check_in_date, self.usr_comments)

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
			userdata = db.query(User).filter_by(username=uname , usr_pwd=passw).first()
			if userdata is not None:
				session['logged_in'] = True
				return redirect(url_for('search'))
			else:
				return 'Invalid Login'
		except:
			return "Invalid Login"

@app.route('/register/', methods=['GET', 'POST'])
def register():
	"""Register Form"""
	if request.method == 'POST':
		new_user = User(first_name=request.form['firstname'], last_name=request.form['lastname'],
		    username=request.form['username'], usr_pwd=request.form['password'])
		db.add(new_user)
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
		loc_data = db.query(Cities).filter(Cities.zipcode.like("%" + search_val + "%")).all()
	elif search_param == 'cityname':
		search_val = search_val.upper()
		loc_data = db.query(Cities).filter(Cities.city_name.like("%" + search_val + "%")).all()

	return render_template("results.html", locations=loc_data)

@app.route("/location")
def location():
	ds_apikey="9a80dd9e0d1a1d0ca8931b3899507105"
	weather = requests.get("https://api.darksky.net/forecast/9a80dd9e0d1a1d0ca8931b3899507105/42.37,-71.11").json()
	return render_template("location.html",weather=weather)

if __name__ == '__main__':
    app.run(debug=True)