from flask import Flask, render_template, request, session, g, jsonify
from flask_session_mysql import MysqlSession
from urllib import parse as urllib_parse
import mysql.connector
import sys
sys.path.insert(0, 'your/path/here')

def multiple_decode(decodee):
    if decodee is None:
        return decodee
    decoded = urllib_parse.unquote(urllib_parse.unquote(decodee))
    return decoded

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['MYSQL_SESSION_HOST'] = 'localhost'
app.config['MYSQL_SESSION_USERNAME'] = 'your_user'
app.config['MYSQL_SESSION_PASSWORD'] = 'your_password'
app.config['MYSQL_SESSION_DATABASE'] = 'your_database'
MysqlSession(app)

@app.before_request
def before_request():
    g.db = mysql.connector.connect(
        user='your_user',
        password='your_password',
        host='localhost',
        database='your_database'
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
    graph_data = []
    if request.method == 'POST':
        query = request.form.get('query')
        pages = request.form.get('pages')
        exclude_below = float(request.form.get('excludeBelow', '0.00'))
        exclude_above = float(request.form.get('excludeAbove', '99999.99'))
        
        # Prevent the numbers from resetting
        session['excludeBelow'] = exclude_below
        session['excludeAbove'] = exclude_above
        
        # Get the checked products to query
        checked_products = [name for name in g.table_names if name in request.form]
        # Make it readable for SQL
        checked_products = [name.replace(" ", "_") for name in checked_products]
        for product in checked_products:
            g.cursor.execute(f"""
                SELECT p.*, '{product}' as table_name
                FROM carousell.{product} p
                INNER JOIN (
                    SELECT name, seller, MAX(date_time) AS max_date_time
                    FROM carousell.{product}
                    WHERE price >= {exclude_below} AND price <= {exclude_above}
                    GROUP BY name, seller
                ) sub_p ON p.name = sub_p.name AND p.seller = sub_p.seller AND p.date_time = sub_p.max_date_time
            """)
            checked_data.extend([(product,) + row for row in g.cursor.fetchall()])
        
        # Store graph data in session
        for product in checked_products:
            g.cursor.execute(f"SELECT * FROM carousell.{product} WHERE price >= {exclude_below} AND price <= {exclude_above}")
            graph_data.extend([(product,) + row for row in g.cursor.fetchall()])
        session_graph_data = [(row[0], float(row[3]), str(row[6]),) for row in graph_data]
        session['graph_checked_data'] = session_graph_data
        
        # To run script
        if query is not None and pages is not None:
            import script7
            script7.run(query, pages)

    return render_template('index.html', table_names=g.table_names, product_data=checked_data)

# Get the data for the modal
@app.route('/product/<table_name>/<name>/<seller>', methods=['GET'])
def product(table_name, name, seller):
    table_name = multiple_decode(table_name)
    name = multiple_decode(name)
    seller = multiple_decode(seller)
    # Historical product data
    g.cursor.execute(f"SELECT * FROM carousell.{table_name} WHERE name = %s AND seller = %s ORDER BY date_time DESC", (name, seller))
    product_data = g.cursor.fetchall()
    # Other products from same seller
    g.cursor.execute(f"SELECT * FROM carousell.{table_name} WHERE seller = %s AND name != %s ORDER BY date_time DESC", (seller, name))
    other_product_data = g.cursor.fetchall()
    # Convert to json and return
    return jsonify({'product_data': product_data, 'other_product_data': other_product_data})

# Gets graph data from session
@app.route('/get_graph_data', methods=['GET'])
def get_graph_data():
    graph_data = session.get('graph_checked_data', [])
    session.pop('graph_checked_data', None)
    return jsonify(graph_data)