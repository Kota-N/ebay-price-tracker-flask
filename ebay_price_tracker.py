from flask import Flask, request, render_template, jsonify, g
import sqlite3
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

DATABASE = '/var/www/html/ebay_price_tracker/db.sqlite'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def home():
    return render_template('index.html')

# tables
@app.route('/tables/products')
def products_table():
    cursor = get_db().cursor()
    product_data = []

    for row in cursor.execute('SELECT * FROM products'):
        product_data.append({'id': row[0], 'name': row[1], 'url': row[2]})

    return jsonify(product_data)

@app.route('/tables/prices')
def prices_table():
    cursor = get_db().cursor()
    price_data = []

    for row in cursor.execute('SELECT * FROM prices'):
        price_data.append(
            {'id': row[0], 'price': row[1], 'product_id': row[2], 'scraped_date': row[3]})

    return jsonify(price_data)

@app.route('/tables/dates')
def dates_table():
    cursor = get_db().cursor()
    date_data = []

    for row in cursor.execute('SELECT * FROM dates'):
        date_data.append(
            {'id': row[0], 'date': row[1]})

    return jsonify(date_data)

# api
@app.route('/api/products')
def get_products():
    db = get_db()
    cursor = db.cursor()

    product_data = []

    for row in cursor.execute('SELECT * FROM products'):
        product_data.append({'id': row[0], 'name': row[1], 'url': row[2]})

    return jsonify(product_data)


@app.route('/api/prices')
def get_prices():
    db = get_db()
    cursor = db.cursor()

    price_data = []

    for row in cursor.execute('SELECT * FROM prices'):
        price_data.append(
            {'id': row[0], 'price': row[1], 'product_id': row[2], 'scraped_date': row[3]})

    return jsonify(price_data)


@app.route('/api/prices/<int:product_id>')
def get_prices_by_id(product_id):
    db = get_db()
    cursor = db.cursor()

    price_data = []

    for row in cursor.execute('SELECT * FROM prices WHERE product_id=' + str(product_id) + ' ORDER BY date(scraped_date) ASC'):
        price_data.append(
            {'id': row[0], 'price': row[1], 'product_id': row[2], 'scraped_date': row[3]})

    return jsonify(price_data)


@app.route('/api/dates')
def get_dates():
    db = get_db()
    cursor = db.cursor()

    date_data = []

    for row in cursor.execute('SELECT * FROM dates ORDER BY date(date) ASC'):
        date_data.append({'id': row[0], 'date': row[1]})

    return jsonify(date_data)

# post
@app.route('/api/products/add', methods=['GET', 'POST'])
def add_product():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'GET':
        return "Hmm... I love it! (404 Not Found)", 404
    else:
        req_data = request.get_json()

        cursor.execute("INSERT INTO products(name, url) VALUES('" + req_data['name'] + "', '" + req_data['url'] + "')")
        db.commit()
        cursor.execute('SELECT * FROM products WHERE name=\'' + req_data['name'] + '\'')


        return jsonify({'added_name': cursor.fetchone()})

@app.route('/api/products/delete', methods=['GET', 'POST'])
def delete_product():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'GET':
        return "Hmm... I love it! (404 Not Found)", 404
    else:
        req_data = request.get_json()

        cursor.execute("SELECT id FROM products WHERE name='" + req_data['name'] + "'")

        id_to_delete = cursor.fetchone()[0]

        cursor.execute("DELETE FROM products WHERE name='" + req_data['name'] + "'")
        db.commit()

        cursor.execute("DELETE FROM prices WHERE product_id=" + str(id_to_delete))
        db.commit()


        return jsonify({'deleted_name': req_data['name']})


if __name__ == '__main__':
    app.run(debug=True)
