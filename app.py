from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from webscrapping.providers import alkosto, linio, falabella, panamericana, mercadolibre
import config	

import re

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

falabella_regex = ".*falabella.*"
alkosto_regex = ".*alkosto.*"
linio_regex = ".*linio.*"
panamericana_regex = ".*panamericana.*"
mercadolibre_regex = ".*mercadolibre.*"

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
    elif(re.search(panamericana_regex, url)):
        response = panamericana.get(url)
    elif(re.search(mercadolibre_regex, url)):
        response = mercadolibre.get(url)
    else:
        return jsonify({"error":"provider not supported"}), 400

    return jsonify(response)

@app.route('/products')
def getAll():
    from webscrapping.models.models import Product
    url = None
    response = None

    url = request.args.get("url")

    if(url != None): 
        url = url.split("?")[0]
        response = jsonify({"products": [x.serialize() for x in Product.query.filter_by(url=url).all()]})
    else:
        response = jsonify({"products": [x.serializeSimple() for x in Product.query.all()]})

    response.status_code = 200
    return response

@app.route('/search')
def search():
    from webscrapping.models.models import Product
    name = None
    response = None

    name = request.args.get("name")

    if(name != None): 
        name = name.split("?")[0]
        response = jsonify({"products": [x.serializeSimple() for x in Product.query.filter(Product.name.like('%' + name + '%'))]})
    else:
        response = jsonify({"products": [x.serializeSimple() for x in Product.query.all()]})

    response.status_code = 200
    return response

@app.route('/update')
def update():
    from webscrapping.models.models import Product
    name = None
    response = None
    
    products = [x.serializeSimple()['url'] for x in Product.query.all()]

    for url in products:
        if(re.search(falabella_regex, url)):
            response = falabella.get(url)
        elif(re.search(alkosto_regex, url)):
            response = alkosto.get(url)
        elif(re.search(linio_regex, url)):
            response = linio.get(url)
        elif(re.search(panamericana_regex, url)):
            response = panamericana.get(url)
        elif(re.search(mercadolibre_regex, url)):
            response = mercadolibre.get(url)

    response=jsonify({"success":True})
    response.status_code = 200
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)