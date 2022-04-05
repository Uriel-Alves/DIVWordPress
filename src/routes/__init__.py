from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from asc.core import session_factory

app = Flask(__name__)
CORS(app)
session = session_factory()

from routes import post



