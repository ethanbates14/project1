import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/search", methods=['GET', 'POST'])
def search():
    locations = db.execute("SELECT * FROM p1_cities ORDER BY state_id, city_name LIMIT 2").fetchall()
    return render_template("search.html",locations=locations)

@app.route("/location")
def location():
    return render_template("location.html")

if __name__ == '__main__':
    app.run(debug=True)