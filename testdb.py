from distutils.command.upload import upload
from urllib import response
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

import os
import sys
from os import environ
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/fyptest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)

uploads_dir = os.path.join('assets/img/donations')


class CarouselItem(db.Model):
    __tablename__ = 'carousel'

    id = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    donorName = db.Column(db.String(50), nullable=False)
    donorAddr = db.Column(db.String(300), nullable=False)
    contactNo = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    requireDelivery = db.Column(db.Integer, nullable=False)
    region = db.Column(db.String(20), nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)
    itemStatus = db.Column(db.String(50), nullable=False)
    fileName = db.Column(db.String(200), nullable=False)

    def __init__(self, id, itemName, description, donorName, donorAddr, contactNo, category, quantity, requireDelivery, region, timeSubmitted, itemStatus, fileName):
        self.id = id
        self.itemName = itemName
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
        self.fileName = fileName

    def json(self):
        return {"id": self.id, "name": self.itemName, "description": self.description, "donorName": self.donorName, "donorAddr": self.donorAddr, "contactNo": self.contactNo, "category": self.category, "quantity": self.quantity, "requireDelivery": self.requireDelivery, "region": self.region, "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus, "fileName": self.fileName}


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
    
class User(db.Model):
    __tablename__ = 'user'
    
    userName = db.Column(db.String, primary_key=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    userType = db.Column(db.String, nullable=False)

    def __init__(self, userName, password, userType):
        self.userName = userName
        self.password = password
        self.userType = userType

    def json(self):
        return {"userName": self.userName, "password": self.password, "userType": self.userType}

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
        formData = request.form
        formDict = formData.to_dict()
        imgFile = request.files['file']
        # print(imgFile)
        itemName = formDict['itemName'].capitalize()
        itemDesc = formDict['itemDesc'].capitalize()
        donorName = formDict['dName'].capitalize()
        donorAddr = formDict['dAddress'].capitalize()
        contactNo = formDict['dContact']
        category = formDict['category'].capitalize()
        quantity = formDict['quantity']
        requireDelivery = formDict['r_Delivery']
        region = formDict['region'].capitalize()

        # Get datetime of donation posting
        now = datetime.now()
        currentDT = now.strftime("%Y-%m-%d %H:%M:%S")
        timeSubmitted = currentDT
        # save file
        fileName = secure_filename(imgFile.filename)
        # print(formDict)
        imgFile.save(os.path.join(uploads_dir, fileName))
        # os.open(uploads_dir+secure_filename(fileName), os.O_RDWR | os.O_CREAT, 0o666)
        file = formDict['itemImg']

        addtodb = CarouselItem(0, itemName, itemDesc, donorName, donorAddr, contactNo, category, quantity, requireDelivery, region, timeSubmitted, "open", file)
        
        try:
            db.session.add(addtodb)
            db.session.commit()
            return jsonify (
                {
                    "code": 200,
                    "message": "Item Successfully added into Donation Listing"
                }
            )
        except Exception as e:
            print(e)
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while adding material :" + str(e)
                }
            ), 500
            
@app.route("/registermw", methods=['POST'])
def register():
        formData = request.form
        formDict = formData.to_dict()
        username = formDict['userName']
        pw = formDict['pw']

        addtodb = User(username, pw, "worker")
        
        try:
            db.session.add(addtodb)
            db.session.commit()
            return jsonify (
                {
                    "code": 200,
                    "message": "Worker successfully added to database!"
                }
            )
        except Exception as e:
            print(e)
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while registering user :" + str(e)
                }
            ), 500



if __name__ == "__main__":
    app.run(port="5004", debug=True)
