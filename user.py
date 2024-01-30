from flask import Flask, render_template, request, g
import sqlite3
from flask import jsonify
from flask import session

app = Flask(__name__)
app.secret_key = 'your secret key here'
DATABASE_FILE_PATH = 'data.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE_FILE_PATH)
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def index():
    with get_db() as conn:
        models = conn.execute("SELECT DISTINCT model FROM scrapped_data").fetchall()
    return render_template('index.html', models=models)

@app.route('/get_options')
def get_options():
    model = request.args.get('model')

    with get_db() as conn:
        colors = conn.execute("SELECT DISTINCT color FROM scrapped_data WHERE model = ?", (model,)).fetchall()
        storage_options = conn.execute("SELECT DISTINCT storage FROM scrapped_data WHERE model = ?", (model,)).fetchall()

    colors = [result[0] for result in colors]
    storage_options = [result[0] for result in storage_options]

    return jsonify(colors=colors, storage=storage_options)

@app.route('/search', methods=['POST'])
def search_prices():
    model = request.form.get('model')
    color = request.form.get('color')
    storage = request.form.get('storage')

    query = f"""
    SELECT s.model, s.storage, s.color, s.price, s.marketplace, p.url 
    FROM scrapped_data  AS s
    JOIN product_url AS p ON s.code = p.code
    WHERE s.model = ?
    """

    parameters = [model]

    if color:
        query += " AND color = ?"
        parameters.append(color)

    if storage:
        query += " AND storage = ?"
        parameters.append(storage)

    query += " ORDER BY s.date DESC, s.price ASC LIMIT 1"

    with get_db() as conn:
        result = conn.execute(query, parameters).fetchone()
    session['search_result'] = result
    return render_template('results.html', result=result)

@app.route('/price-trend', methods=['POST'])
def price_trend():
    result = session.get('search_result')

    query = f"""
    SELECT s.date, s.price
    FROM scrapped_data AS s
    JOIN product_url AS p ON s.code = p.code
    WHERE s.model = ? AND s.marketplace = ? AND s.color = ? AND s.storage = ?
    """

    parameters = [result[0], result[4], result[2], result[1]]

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        column_names = [description[0] for description in cursor.description]
        result = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    

    return jsonify(result = result)

if __name__ == '__main__':
    app.run(debug=True)
