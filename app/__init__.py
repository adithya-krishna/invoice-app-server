from flask import Flask
from flask.ext.cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TestTest';
app.config['CORS_HEADERS'] = 'Content-Type';
cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:5000"}})

from . import db, routes

# db.init_db(app)