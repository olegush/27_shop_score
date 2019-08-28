import os
import json
from datetime import datetime, timedelta
from io import BytesIO
from base64 import b64encode

from dotenv import load_dotenv
from flask import Flask, send_from_directory, request, render_template
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt


load_dotenv()

PG_HOST = os.environ.get('PG_HOST')
PG_PORT = os.environ.get('PG_PORT')
PG_DB = os.environ.get('PG_DB')
PG_TABLE = os.environ.get('PG_TABLE')
PG_USER = os.environ.get('PG_USER')
PG_PWD = os.environ.get('PG_PWD')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{PG_USER}:{PG_PWD}@{PG_HOST}:{PG_PORT}/{PG_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.Model.metadata.reflect(bind=db.engine)


class Order(db.Model):
    __table__ = db.Model.metadata.tables[PG_TABLE]


def get_img(plt):
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    img = b64encode(buffer.getvalue()).decode('utf-8').strip()
    buffer.close()
    return img


@app.route('/')
def score():
    NOW = datetime.now()
    TIME_UNIT = os.environ.get('TIME_UNIT')
    TIME_MULT = int(os.environ.get('TIME_MULT'))
    TIME_LIMITS = json.loads(os.environ['TIME_LIMITS'])
    TIME_BOUND = (NOW - timedelta(hours=TIME_LIMITS[-1][-1])).replace(microsecond=0)
    colors = ['green', 'yellow', 'red']
    labels = []
    sizes = []

    orders = Order.query.filter(Order.created > TIME_BOUND).order_by(Order.created.desc())
    unconfirmed_orders = list(orders.filter(Order.confirmed == None))

    # Filter orders by time intervals
    for lower, upper in TIME_LIMITS:
        sizes.append(len(list(filter(
                                lambda x: x.created <= NOW - timedelta(seconds=lower*TIME_MULT) \
                                and x.created > NOW - timedelta(seconds=upper*TIME_MULT),
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
                TIME_LIMIT_MAX=TIME_LIMITS[-1][-1],
                TIME_UNIT=TIME_UNIT,
                orders_tail=orders[:30],
                total_orders=len(list(orders)),
                total_unconfirmed_orders=len(unconfirmed_orders),
                img=get_img(plt))

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')
