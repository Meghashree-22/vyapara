import pymongo
from bson.json_util import dumps
import json
from flask import Flask, request, render_template, session, redirect, url_for, flash, Response, abort, render_template_string, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = b'\xd2(*K\xa0\xa8\x13]g\x1e9\x88\x10\xb0\xe0\xcc'

#Loads the Database and Collections
mongo = pymongo.MongoClient('mongodb+srv://admin:admin@cluster0-dlnod.gcp.mongodb.net/test?retryWrites=true&w=majority', maxPoolSize=50, connect=True)
db = pymongo.database.Database(mongo, 'vyapara')

@app.route('/')
def test():
    return "Works"


@app.route('/api/new_buyer', methods=['POST'])
def new_buyer():
    inputData = request.json
    Buyer_Data = pymongo.collection.Collection(db, 'Buyer_Data')
    for i in json.loads(dumps(Buyer_Data.find())):
        if i['email'] == inputData['email']:
            return Response(status=403)
    Buyer_Data.insert_one({'email':inputData['email'],'password':inputData['password']});
    return Response(status=200)


@app.route('/api/new_seller', methods=['POST'])
def new_seller():
    inputData = request.json
    Seller_Data = pymongo.collection.Collection(db, 'Seller_Data')
    for i in json.loads(dumps(Seller_Data.find())):
        if i['email'] == inputData['email']:
            return Response(status=403)
    Seller_Data.insert_one({'email':inputData['email'],'password':inputData['password']});
    return Response(status=200)


@app.route('/api/login_buyer', methods=['POST'])
def login_buyer():
    inputData = request.json
    Buyer_Data = pymongo.collection.Collection(db, 'Buyer_Data')
    for i in json.loads(dumps(Buyer_Data.find())):
        if i['email'] == inputData['email'] and i['password'] == inputData['password']:
            return Response(status=200)
        else:
            return Response(status=403)


@app.route('/api/login_seller', methods=['POST'])
def login_seller():
    inputData = request.json
    Seller_Data = pymongo.collection.Collection(db, 'Seller_Data')
    for i in json.loads(dumps(Seller_Data.find())):
        if i['email'] == inputData['email'] and i['password'] == inputData['password']:
            return Response(status=200)
        else:
            return Response(status=403)


@app.route('/api/add_new_product', methods=['POST'])
def add_new_product():
    inputData = request.json
    Product_Data = pymongo.collection.Collection(db, 'Product_Data')
    Seller_Data = pymongo.collection.Collection(db, 'Seller_Data')
    for i in json.loads(dumps(Seller_Data.find())):
        if i['email'] == inputData['email']:
            Product_Data.insert_one({'seller':inputData['email'],'name':inputData['name'],'price':inputData['price'],'description':inputData['description']})
            return Response(status=200)
    return Response(status=403)


@app.route('/api/add_new_sale', methods=['POST'])
def add_new_sale():
    inputData = request.json
    Product_Data = pymongo.collection.Collection(db, 'Product_Data')
    Buyer_Data = pymongo.collection.Collection(db, 'Buyer_Data')
    for i in json.loads(dumps(Buyer_Data.find())):
        if i['email'] == inputData['email']:
            Sales_Data.insert_one({'product':inputData['product_id'],'buyer':inputData['email'],'date':inputData['date']})
            return Response(status=200)
    return Response(status=403)
