import flask
import psycopg2
import psycopg2.extras
import collections
from flask import abort, jsonify

app = flask.Flask(__name__)
app.config['DEBUG'] = True

# connect tom the db
conn = None

# for office
try:
    with psycopg2.connect(
        host = 'localhost',
        database = 'test',
        user = 'postgres',
        password = 'password',
        port = 5432) as conn:

        # cursor
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            hotels = []
            cur.execute('SELECT * FROM hotels_content')
            rows = cur.fetchall()
            for record in rows:
                d = collections.OrderedDict()
                d['id']         = record['id']
                d['title']      = record['title']
                d['price']      = record['price']
                d['review']     = record['review']
                d['location']   = record['location']
                d['amenities']  = record['amenities']
                d['image_link'] = record['image_link']
                hotels.append(d)

except Exception as error:
    print(error)
finally:
    # finally will execute with or wiothout any error bcz if and error occurs, the try block stops.

    if conn is not None:
        # close the connection
        conn.close()

@app.route('/', methods=['GET'])
def honme():
    return '''<h1>Dubai hotels</h1>
<p>this site is a prototype api for Dubai Hotels.</p>'''

# A route to return all of the available entries in our catalog
@app.route('/hotels', methods=['GET'])
def api_all():
    return flask.jsonify(hotels)

@app.route('/hotels/<int:id>')
def api_id(id):
    if id > len(hotels) or id < len(hotels):
        return "Error: id invalid"

    results = []
    for hotel in hotels:
        if hotel['id'] == id:
            results.append(hotel)
    return jsonify(results)

app.run()
