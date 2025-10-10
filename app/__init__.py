from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)



DATABASE = 'databse/sample.db'

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection():
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


#app routing

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/database")
def database():
    cur = get_db.cursor()

