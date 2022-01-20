from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import os
import sys
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/fyptest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)


class CarouselItem(db.Model):
    __tablename__ = 'carousel'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    donorName = db.Column(db.String(50), nullable=False)
    donorAddr = db.Column(db.String(300), nullable=False)
    contactNo = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    requireDelivery = db.Column(db.Integer, nullable=False)
    region = db.Column(db.String(20), nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)
    itemStatus = db.Column(db.Integer, nullable=False)
    fileName = db.Column(db.String(200), nullable=False)

    def __init__(self, name, description, donorName, donorAddr, contactNo, category, quantity, requireDelivery, region, timeSubmitted, itemStatus, filename):
        self.name = name
        self.description = description
        self.donorName = donorName
        self.donorAddr = donorAddr
        self.contactNo = contactNo
        self.category = category
        self.quantity = quantity
        self.requireDelivery = requireDelivery
        self.region = region
        self.timeSubmitted = timeSubmitted
        self.itemStatus = itemStatus
        self.filename = filename

    def json(self):
        return {"id": self.id, "name": self.name, "description": self.description, "donorName": self.donorName, "donorAddr": self.donorAddr, "contactNo": self.contactNo, "category": self.category, "quantity": self.quantity, "requireDelivery": self.requireDelivery, "region": self.region, "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus, "fileName": self.fileName}


# class Category(db.Model):
#     __tablename__ = 'category'

#     categoryName = db.Column(db.String, primary_key=True)
#     description = db.Column(db.String, nullable=True)

#     def __init__(self, categoryName, description):
#         self.categoryName = categoryName
#         self.description = description

#     def json(self):
#         return {"categoryName": self.categoryName, "description": self.description}

class CategoryItem(db.Model):
    __tablename__ = 'categoryitem'

    itemId = db.Column(db.Integer, nullable=False)
    itemName = db.Column(db.String, primary_key=True)
    attachedCategory = db.Column(db.String, primary_key=True)

    def __init__(self, itemName, attachedCategory):
        self.itemName = itemName
        self.attachedCategory = attachedCategory

    def json(self):
        return {"itemId": self.itemId, "itemName": self.itemName, "attachedCategory": self.attachedCategory}

# get all items submitted by donors where timeSubmitted > 0 and timeSubmitted <= 24 (time logic not done)


@app.route("/getItems")
def getAllItems():
    carouselList = CarouselItem.query.all()
    # print(carouselList)
    if len(carouselList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "items": [carouselItem.json() for carouselItem in carouselList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no donations at the moment."
        }
    ), 404

# get item by id where timeSubmitted > 0 and timeSubmitted <= 24 (time logic not done)


@app.route("/getItemById/<id>")
def getItem(id):
    itemInfo = CarouselItem.query.filter_by(id=id)
    # print(carouselList)
    if (itemInfo):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "itemDetail": [item.json() for item in itemInfo]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Item ID does not seem to exist."
        }
    ), 404


# @app.route("/addItemToCarousel", methods=['POST'])
# def addCarouselItem():
#     formData = request.form
#     formDict = formData.to_dict()


# get all items submitted by donors where timeSubmitted > 0 and timeSubmitted <= 24 and filtered by category (time logic not done)
@app.route("/getItem/<Cat>")
def getItemsByCategory(Cat):
    itemList = CarouselItem.query.filter_by(category=Cat)
    if len(itemList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "itemsByCat": [carouselItem.json() for carouselItem in itemList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no items listed under this category."
        }
    ), 404

# get all exisitng categories to be displayed in drop down fields


@app.route("/getCat")
def getAllCat():
    categoryList = CategoryItem.query.with_entities(
        CategoryItem.attachedCategory).distinct()
    # print(categoryList)
    if (categoryList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    # No need for .json() because you are returning just one column's data
                    "categories": [category for category in categoryList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Please make sure the py file is being run to see category list"
        }
    ), 404

# get all exisitng categories to be displayed in drop down fields


@app.route("/getItemsInCat/<cat>")
def getItemsInCategory(cat):
    itemsInCategory = CategoryItem.query.filter_by(attachedCategory=cat)
    # print(itemsInCategory)

    if (itemsInCategory):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "itemsInCat": [item.json() for item in itemsInCategory]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Please make sure the py file is running to view items in each category."
        }
    ), 404

# API to add item into carousel table from donor form


@app.route("/addDonation", methods=['POST'])
def addCarouselItem():
    if request.method == 'POST':
        itemname = request.form.get('itemName')
        description = request.form.get('itemDesc')
        donorName = request.form.get('dName')
        donorAddr = request.form.get('dAddress')
        contactNo = request.form.get('dContact')
        category = request.form.get('category')
        quantity = request.form.get('quantity')
        requireDelivery = request.form.get('r_Delivery')
        region = request.form.get('region')
        timeSubmitted = request.form.get('timeSubmitted')
        itemStatus = request.form.get('itemStatus')
        fileName = request.form.get('itemImg')


if __name__ == "__main__":
    app.run(port="5004", debug=True)
