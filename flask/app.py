from flask import Flask, flash, redirect, render_template, request, session, g
from flask_session import Session
import datetime
from flask_session_mysql import MysqlSession
import mysql.connector
import plotly.graph_objects as go
import plotly.offline as pyo
import sys
sys.path.insert(0, 'C:/Users/jianr/OneDrive/Desktop/WebScraper')

app = Flask(__name__)
app.secret_key = '762fb1fb00d802953dad68bcffe1e574caada6b85ec37139'
app.config['MYSQL_SESSION_HOST'] = 'localhost'
app.config['MYSQL_SESSION_USERNAME'] = 'jianrontan'
app.config['MYSQL_SESSION_PASSWORD'] = 'Jianron101032%&g'
app.config['MYSQL_SESSION_DATABASE'] = 'carousell'
MysqlSession(app)

@app.before_request
def before_request():
    g.db = mysql.connector.connect(
        user='jianrontan',
        password='Jianron101032%&g',
        host='localhost',
        database='carousell'
    )
    g.cursor = g.db.cursor()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'cursor'):
        g.cursor.close()
    if hasattr(g, 'db'):
        g.db.close()

# index.html
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query = request.form['query']
        
        import script7
        script7.run(query)

    return render_template('index.html')