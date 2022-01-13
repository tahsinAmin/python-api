from crypt import methods
import flask
import psycopg2
import psycopg2.extras
import collections
from flask import abort, jsonify, request

app = flask.Flask(__name__)
app.config['DEBUG'] = True

def getHotels(qry):
    # connect to the db
    conn = None
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
                cur.execute(qry)
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
                
                return hotels

    except Exception as error:
        print(error)
    finally:
        # finally will execute with or without any error bcz if and error occurs, the try block stops.

        if conn is not None:
            # close the connection
            conn.close()

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Dubai hotels</h1>
<p>this site is a prototype api for Dubai Hotels.</p>'''

# A route to return all of the available entries in our catalog
@app.route('/hotels/all', methods=['GET'])
def api_all():
    hotels = getHotels('SELECT * FROM hotels_content')
    return flask.jsonify(hotels)

@app.route('/hotels', methods=['GET'])
def api_filter():
    query_params = request.args
    
    id        = query_params.get('id')
    amenities_items = query_params.get('amenities')
    amenities = amenities_items.split()
    price     = query_params.get('price')
    

    query = "SELECT * FROM hotels_content WHERE"

    if id:
        query+=f' id={id} AND'
    if amenities:
        for item in amenities:
            query+=f" amenities like '%{item.capitalize()}%' AND"
    if price:
        query+=f' price>={price} AND'
    if not (id or amenities or price):
        return "Nothing is given."
    
    query = query[:-4]
    print(query)
    hotels = getHotels(query)

    return flask.jsonify(hotels)

app.run()
