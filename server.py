import os
from datetime import datetime, timedelta
from itertools import filterfalse, groupby
from io import BytesIO
from base64 import b64encode

from dotenv import load_dotenv
from flask import Flask, send_from_directory, request, render_template
import psycopg2.extras
import psycopg2
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route('/')
def score():
    return render_template('score.html')

load_dotenv()

PG_HOST = os.environ.get('PG_HOST')
PG_PORT = os.environ.get('PG_PORT')
PG_DB = os.environ.get('PG_DB')
PG_USER = os.environ.get('PG_USER')
PG_PWD = os.environ.get('PG_PWD')
'''
NOW = datetime.now()
TIME_UNIT = 'hour'
TIME_MULT = 60 * 60
TIME_LIMIT_MAX = 240
INTERVALS = [(0, 80), (80, 160), (160, TIME_LIMIT_MAX)]
TIME_BOUND = (NOW - timedelta(hours=TIME_LIMIT_MAX)).replace(microsecond=0)


def get_img(plt):
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    img = b64encode(buffer.getvalue()).decode('utf-8').strip()
    buffer.close()
    return img


@app.route('/')
def score():
    colors = ['green', 'yellow', 'red']
    labels = []
    sizes = []

    # Connect to db and get unconfirmed orders
    conn = psycopg2.connect(host=PG_HOST, port=PG_PORT, database=PG_DB, user=PG_USER, password=PG_PWD)
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        query = "SELECT * " \
                "FROM orders " \
                "WHERE created > '{}' " \
                "ORDER BY created DESC ".format(TIME_BOUND)
        cursor.execute(query)
        result = cursor.fetchall()
    unconfirmed_orders = list(filterfalse(lambda x: x['confirmed'], result))

    # Filter orders by time intervals
    for lower, upper in INTERVALS:
        sizes.append(len(list(filter(
                                lambda x: x['created'] <= NOW - timedelta(seconds=lower*TIME_MULT) \
                                and x['created'] > NOW - timedelta(seconds=upper*TIME_MULT),
                                unconfirmed_orders))))
        labels.append(f'{lower} to {upper} {TIME_UNIT}s')

    # Draw the pie chart
    plt.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct=lambda v: '{:.0f}'.format(v * len(unconfirmed_orders) / 100))

    return render_template(
                'index.html',
                TIME_LIMIT_MAX=TIME_LIMIT_MAX,
                TIME_UNIT=TIME_UNIT,
                total_orders=len(result),
                total_unconfirmed_orders=len(unconfirmed_orders),
                img=get_img(plt))


@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')
'''

if __name__ == "__main__":
    load_dotenv()
    host = os.environ.get('HOST')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)
