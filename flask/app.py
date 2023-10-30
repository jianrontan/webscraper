from flask import Flask, flash, redirect, render_template, request, session, g, jsonify
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
    g.cursor.execute("SHOW TABLES;")
    table_names = [table[0] for table in g.cursor.fetchall() if table[0] != "sessions"]
    table_names = [name.replace("_", " ") for name in table_names]
    g.table_names = table_names

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'cursor'):
        g.cursor.close()
    if hasattr(g, 'db'):
        g.db.close()

# index.html
@app.route('/', methods=['GET', 'POST'])
def home():
    checked_data = []
    if request.method == 'POST':
        query = request.form.get('query')
        pages = request.form.get('pages')
        
        checked_products = [name for name in g.table_names if name in request.form]
        checked_products = [name.replace(" ", "_") for name in checked_products]
        for product in checked_products:
            g.cursor.execute(f"""
                SELECT p.*, '{product}' as table_name
                FROM carousell.{product} p
                INNER JOIN (
                    SELECT name, seller, MAX(date_time) AS max_date_time
                    FROM carousell.{product}
                    GROUP BY name, seller
                ) sub_p ON p.name = sub_p.name AND p.seller = sub_p.seller AND p.date_time = sub_p.max_date_time
            """)
            checked_data.extend([(product,) + row for row in g.cursor.fetchall()])
        
        if query is not None and pages is not None:
            import script7
            script7.run(query, pages)

    return render_template('index.html', table_names=g.table_names, product_data=checked_data)

@app.route('/product/<table_name>/<name>/<seller>', methods=['GET'])
def product(table_name, name, seller):
    # Historical product data
    g.cursor.execute(f"SELECT * FROM carousell.{table_name} WHERE name = %s AND seller = %s ORDER BY date_time DESC", (name, seller))
    product_data = g.cursor.fetchall()
    # Other products from same seller
    g.cursor.execute(f"SELECT * FROM carousell.{table_name} WHERE seller = %s AND name != %s ORDER BY date_time DESC", (seller, name))
    other_product_data = g.cursor.fetchall()
    # Convert to json and return
    return jsonify({'product_data': product_data, 'other_product_data': other_product_data})