from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from webscrapping.providers import alkosto, linio, falabella
import config	

import re

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)	

falabella_regex = ".*falabella.*"
alkosto_regex = ".*alkosto.*"
linio_regex = ".*linio.*"

@app.route('/track')
def track():
    url = request.args.get("url")
    response = {}

    if(re.search(falabella_regex, url)):
        response = falabella.get(url)
    elif(re.search(alkosto_regex, url)):
        response = alkosto.get(url)
    elif(re.search(linio_regex, url)):
        response = linio.get(url)
    else:
        return jsonify({"error":"provider not supported"}), 400

    return jsonify(response)