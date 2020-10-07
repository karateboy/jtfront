import io
import sys
import json
# import requests

from flask import Flask, request, render_template
from flask_pymongo import PyMongo
from datetime import datetime
from flask_cors import CORS

import map2Mongo as m2m

# from bson.json_util import dumps
# from bson import ObjectId
# from bs4 import BeautifulSoup# from mongoengine_jsonencoder import MongoEngineJSONEncoder
# import urllib.request


# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

app = Flask(__name__)
# app.after_request(after_request)
# app.config["MONGO_URI"] = "mongodb://192.168.100.36:27017/jdb"
# mongo = PyMongo(app)
CORS(app)

#
# python5000 -> php:7070  because mysql unicode problem on php
# Getting data from MYSQL as 1 document grouping
#

# class Encoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, ObjectId):
#             return str(obj)
#         elif isinstance(obj, datetime):
#             return obj.__str__()
#         else:
#             return obj


#
#
#     if request.method == 'GET':
#    elif request.method == 'POST':
#    else:


###################################
# Customer
###################################

@app.route("/mysql/customer", methods=['GET', 'POST'])
def mysql_customerlist():
    if request.method == 'GET':
        customer = m2m.jdbCustomer("0")
        document = customer.get_list(customer)

        return customer.output_encoded()
    elif request.method == 'POST':
        print("POST", file=sys.stderr)
    else:
        abort(400)


@app.route("/mysql/customer/<id>", methods=['GET', 'PUT'])
def mysql_customer(id):
    customer = m2m.jdbCustomer(id)
    if request.method == 'GET':
        document = customer.get_document()
        forceUpdate = request.args.get('force')
        jobUpdate = request.args.get('job')

        if (document is None or forceUpdate == "1"):
            print("mysql", file=sys.stderr)
            document = customer.get_fromMysql()
        else:
            print("mongo", file=sys.stderr)

        if(jobUpdate == "1"):
            customer.get_jobs_summary()

        return customer.output_encoded()

    elif request.method == 'POST':
        print("POST", file=sys.stderr)
    else:
        abort(400)


###################################
# Product
###################################


@app.route("/mysql/product", methods=['GET', 'POST'])
def mysql_productlist():
    if request.method == 'GET':
        product = m2m.jdbProduct("0")
        customer = request.args.get('customer')

        if(customer is None):
            document = product.get_list("0")
        else:
            document = product.get_list(customer)

        return product.output_encoded()

    elif request.method == 'POST':
        print("POST", file=sys.stderr)

    else:
        abort(400)


@app.route("/mysql/product/<id>", methods=['GET', 'PUT'])
def mysql_product(id):
    product = m2m.jdbProduct(id)
    document = product.get_document()
    forceUpdate = request.args.get('force')
    jobUpdate = request.args.get('job')

    if (document is None or forceUpdate == "1"):
        print("mysql", file=sys.stderr)
        document = product.get_fromMysql()
    else:
        print("mongo", file=sys.stderr)

    if(jobUpdate == "1"):
        product.get_jobs_summary()

    return product.output_encoded()


###################################
# Work
###################################


@app.route("/mysql/work", methods=['GET', 'POST'])
def mysql_worklist():
    if request.method == 'GET':
        work = m2m.jdbWork("0")
        customer = request.args.get('customer')

        if(customer is None):
            document = work.get_list("0")
        else:
            document = work.get_list(customer)

        return work.output_encoded()

    elif request.method == 'POST':
        print("-"*60, file=sys.stderr)
        # print("Posted", file=sys.stderr)
        p = request.get_json()
        print(p, file=sys.stderr)
        print("-"*60, file=sys.stderr)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        work = m2m.jdbWork("0")
        # work.post_document({'test':1123})
        return resp
    
    else:
       abort(400)

# @app.route("/mysql/work", methods=['POST'])
# # @cross_origin(origin='localhost',headers=['Content- Type','*'])
# def post_order():
#     if request.method == 'POST':
#         print("-"*60, file=sys.stderr)
#         print("Posted", file=sys.stderr)
#         p = request.get_json()
#         print(p, file=sys.stderr)
#         print("-"*60, file=sys.stderr)
#     resp = app.make_response("hello")
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     work = m2m.jdbWork("0")
#     # work.post_document({'test':1123})
#     return resp
    

@app.route("/mysql/work/<id>", methods=['GET', 'PUT'])
def mysql_work(id):
    work = m2m.jdbWork(id)
    document = work.get_document()
    forceUpdate = request.args.get('force')

    if (document is None or forceUpdate == "1"):
        print("force", file=sys.stderr)
        document = work.get_fromMysql()
    else:
        print("mongo", file=sys.stderr)

    return work.output_encoded()




###################################
# Order
###################################

@app.route("/mysql/order", methods=['GET', 'POST'])
def mysql_orderlist():
    order = m2m.jdbOrder("0")
    customer = request.args.get('customer')

    if(customer is None):
        document = order.get_list("0")
    else:
        document = order.get_list(customer)

    return order.output_encoded()


@app.route("/mysql/order/<id>", methods=['GET', 'PUT'])
def mysql_order(id):
    order = m2m.jdbOrder(id)
    document = order.get_document("jobs")
    forceUpdate = request.args.get('force')

    if (document is None or forceUpdate == "1"):
        print("force", file=sys.stderr)
        document = order.get_fromMysql("jobs")
    else:
        print("mongo", file=sys.stderr)

    return order.output_encoded()

@app.route("/mysql/order/<id>", methods=['PUT'])
def update_order(id):
    order = m2m.jdbOrder(id)
    order.patch_document
    return



###################################
# Material
###################################

@app.route("/mysql/material", methods=['GET', 'POST'])
def mysql_materiallist():
    material = m2m.jdbMaterial("0")
    document = material.get_list()

    return material.output_encoded()


@app.route("/mysql/material/<id>", methods=['GET', 'PUT'])
def mysql_material(id):
    material = m2m.jdbMaterial(id)
    document = material.get_document()
    forceUpdate = request.args.get('force')

    if (document is None or forceUpdate == "1"):
        print("force", file=sys.stderr)
        document = material.get_fromMysql()
    else:
        print("mongo", file=sys.stderr)

    return material.output_encoded()

# @app.route("/mysql/test/time")
# def mysql_test():
#     test = m2m.MysqlJsonApi()
#     time = test.format_isodate("2020-01-01")
#     return str(time)



if __name__ == '__main__':
    # app.run(host='192.168.100.36',debug=True)
    app.run(host='127.0.0.1', debug=True)
    app.after_request(after_request)
