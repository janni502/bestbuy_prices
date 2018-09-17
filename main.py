# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging

import requests
# from datetime import datetime, timedelta

from google.appengine.ext import ndb
import json

from flask import Flask, render_template
from Product.model import Product

app = Flask(__name__)


@app.route('/hello')
def hello():
    return render_template('base.html')


@app.route('/get')
def get():
    # get all products data from the ndb database
    data = Product.query().fetch()

    return render_template('productslist.html', data=data)


@app.route('/test/<string:product_key>')
def single_product (product_key):
    # get all products data from the ndb database
    key = ndb.Key(urlsafe=product_key)
    product = key.get()

    return render_template('singleProduct.html', product=product)


@app.route('/products', methods=['POST'])
def create_product():
    response = requests.get(
        'https://api.bestbuy.com/v1/products((categoryPath.id=abcat0502000))?apiKey=KLhDAB2JWXAr57Y8ZLSrkV7U&format=json')
    data = response.json()

    for p in data["products"]:
        product_entity = Product.get_by_id(p["sku"])
        # if the entity is exist in the database,
        # need to add the new price to prices if the price change from last record
        # need to check if it is the new lowest price, if so update the lowest_price

        if product_entity:

            if product_entity.prices[-1]["price"] != p["salePrice"]:
                product_entity.prices.append({"date": p["priceUpdateDate"], "price": p["salePrice"]})

                if p["salePrice"] < product_entity.lowest_price:
                    product_entity.lowest_price={"start_date": p["priceUpdateDate"], "price": p["salePrice"]}
                    product_entity.put()
                if p["salePrice"] > product_entity.highest_price:
                    product_entity.highest_price={"start_date": p["priceUpdateDate"], "price": p["salePrice"]}
            product_entity.put()


        else:
            new_product = Product(id=p["sku"],
                              name=p["name"],
                              categoryPath = p['categoryPath'],
                              prices=[{"date": p["priceUpdateDate"], "price": p["salePrice"]}],
                              lowest_price ={"date": "2018-9-1", "price": 199},
                              highest_price = {"date": "2018-9-1", "price": 199}


            )
            new_product.put()

        continue
    return '', 200


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
