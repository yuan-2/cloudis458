from distutils.command.upload import upload
from urllib import response
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import bcrypt

import os
import sys
from os import environ
from sqlalchemy import ForeignKey
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
    donorAddr = db.Column(db.String(300), nullable=False)
    contactNo = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    subCat = db.Column(db.String(30), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    requireDelivery = db.Column(db.Integer, nullable=False)
    region = db.Column(db.String(20), nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)
    itemStatus = db.Column(db.String(50), nullable=False)
    fileName = db.Column(db.String(200), nullable=False)

    def __init__(self, id, itemName, donorAddr, contactNo, category, subCat, quantity, requireDelivery, region, timeSubmitted, itemStatus, fileName):
        self.id = id
        self.itemName = itemName
        self.donorAddr = donorAddr
        self.contactNo = contactNo
        self.category = category
        self.subCat = subCat
        self.quantity = quantity
        self.requireDelivery = requireDelivery
        self.region = region
        self.timeSubmitted = timeSubmitted
        self.itemStatus = itemStatus
        self.fileName = fileName

    def json(self):
        return {"id": self.id, "itemName": self.itemName, "donorAddr": self.donorAddr, "contactNo": self.contactNo, "category": self.category, "subcat": self.subCat, "quantity": self.quantity, "requireDelivery": self.requireDelivery, "region": self.region, "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus, "fileName": self.fileName}

class WishList(db.Model):
    __tablename__ = 'wishlist'
    
    id = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.String(300))
    category = db.Column(db.String(50), nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)
    itemStatus = db.Column(db.String(50), nullable=False)
    
    def __init__(self, id, itemName, quantity, remarks, category, timeSubmitted, itemStatus):
        self.id = id
        self.itemName = itemName
        self.quantity = quantity
        self.remarks = remarks
        self.category = category
        self.timeSubmitted = timeSubmitted
        self.itemStatus = itemStatus
        
    def json(self):
        return {"id": self.id, "itemName": self.itemName, "quantity": self.quantity, "remarks": self.remarks, "category": self.category, "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus}
        
    

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

    itemId = db.Column(db.Integer, nullable=False, primary_key=True)
    itemName = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    subCat = db.Column(db.String, nullable=False)

    def __init__(self, itemId, itemName, category, subCat):
        self.itemId = itemId
        self.itemName = itemName
        self.category = category
        self.subCat = subCat

    def json(self):
        return {"itemId": self.itemId, "itemName": self.itemName, "category": self.category, "subCat": self.subCat}
    
class User(db.Model):
    __tablename__ = 'user'
    
    username = db.Column(db.Integer, primary_key=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    userType = db.Column(db.String(20), nullable=False)

    def __init__(self, username, password, userType):
        self.username = username
        self.password = password
        self.userType = userType

    def json(self):
        return {"username": self.username, "password": self.password, "userType": self.userType}

class Request(db.Model):
    __table__ = 'request'
    
    reqId = db.Column(db.Integer, primary_key=True, nullable=False)
    requestorContactNo = db.Column(db.Integer, nullable=False)
    deliveryLocation = db.Column(db.String(300), nullable=False)
    itemId = db.Column(db.Integer, nullable=False)
    requestQty = db.Column(db.Integer, nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)
    
    def __init__(self, reqId, requestorContactNo, deliveryLocation, itemId, requestQty, timeSubmitted):
        self.reqId = reqId
        self.requestorContactNo = requestorContactNo
        self.deliveryLocation = deliveryLocation
        self.itemId = itemId
        self.requestQty = requestQty
        self.timeSubmitted = timeSubmitted
        
    def json(self):
        return {"reqId": self.reqId, "requestorContactNo": self.requestorContactNo, "deliveryLocation": self.deliveryLocation, "itemId": self.itemId, "requestQty": self.requestQty, "timeSubmitted": self.timeSubmitted}


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
    
@app.route("/getItemsBySubCat/<subcat>")
def filterItems(subcat):
    carouselList = CarouselItem.query.filter_by(subCat=subcat)
    # print(carouselList)
    if (carouselList or len(carouselList)):
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
            "message": "There are no items donated under this Sub-category"
        }
    ), 404
    
    
@app.route("/getWL")
def getWishListItems():
    wishList = WishList.query.all()
    if len(wishList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "items": [wishListitem.json() for wishListitem in wishList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Wishlist is currently empty."
        }
    ), 404

# get item by id where timeSubmitted > 0 and timeSubmitted <= 24 (time logic not done)


@app.route("/getItemById/<id>")
def getItem(id):
    itemInfo = CarouselItem.query.filter_by(id=id)
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
# API for search function
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
        CategoryItem.category).distinct()
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

@app.route("/getSubCat/<cat>")
def getSubCat(cat):
    subCats = CategoryItem.query.filter_by(category=cat)
    
    if (subCats):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "subcats": [subcat.json() for subcat in subCats]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Error retrieving Subcatogories."
        }
    ), 404

@app.route("/getItemsInSubCat/<subcat>")
def getItemsInSubCat(subcat):
    itemsInCategory = CategoryItem.query.filter_by(subCat=subcat)
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
            "message": "Error retreiving Items in Subcategories."
        }
    ), 404


# API to add item into carousel table from donor form


@app.route("/addDonation", methods=['POST'])
def addCarouselItem():
        formData = request.form
        formDict = formData.to_dict()
        imgFile = request.files['file']
        itemName = formDict['itemName'].capitalize()
        donorAddr = formDict['dAddress'].capitalize()
        contactNo = formDict['dContact']
        category = formDict['category'].capitalize()
        subCat = formDict['subcat'].capitalize()
        quantity = formDict['quantity']
        requireDelivery = formDict['r_Delivery']
        region = formDict['region'].capitalize()

        # Get datetime of donation posting
        now = datetime.now()
        currentDT = now.strftime("%Y-%m-%d %H:%M:%S")
        timeSubmitted = currentDT
        # save file
        fileName = secure_filename(imgFile.filename.replace(" ", ""))
        # print(formDict)
        imgFile.save(os.path.join(uploads_dir, fileName))
        # os.open(uploads_dir+secure_filename(fileName), os.O_RDWR | os.O_CREAT, 0o666)
        file = formDict['itemImg']

        addtodb = CarouselItem(0, itemName, donorAddr, contactNo, category, subCat, quantity, requireDelivery, region, timeSubmitted, "open", file)
        
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
                    "message": "An error occurred while adding donation, please try again later"
                }
            ), 500
            
@app.route("/addRequest", methods=['POST'])
def addNewRequest():
        formData = request.form
        formDict = formData.to_dict()
        id = formDict['id']
        destination = formDict['destination'].capitalize()
        contact = formDict['contact']
        iQuantity = formDict['iQuantity']

        # Get datetime of donation posting
        now = datetime.now()
        currentDT = now.strftime("%Y-%m-%d %H:%M:%S")
        timeSubmitted = currentDT

        addtodb = Request(0, contact, destination, id, iQuantity, timeSubmitted)
        
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
                    "message": "An error occurred while adding donation, please try again later"
                }
            ), 500
            
@app.route("/registermw", methods=['POST'])
def register():
        formData = request.form
        formDict = formData.to_dict()
        username = formDict['userName']
        pw = formDict['pw']
        hashedpw = bcrypt.hashpw(str(pw).encode('utf-8'), bcrypt.gensalt())

        addtodb = User(username, hashedpw, "worker")
        
        try:
            db.session.add(addtodb)
            db.session.commit()
            return jsonify (
                {
                    "code": 200,
                    "message": "Worker account successfully created!"
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
            
@app.route("/login", methods=['POST'])
def checkLogin():
    formData = request.form
    formDict = formData.to_dict()
    uName = formDict["username"]
    pw = formDict["password"]
    
    user = User.query.filter_by(username=uName).first()
    if (user != None):
        if (bcrypt.checkpw(str(pw).encode('utf-8'), str(user.password).encode('utf-8'))):
        
            print("Password checks out")
    
        
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "message": "Authentication success!",
                        "userType": user.json()
                    }
                }
            )
        return jsonify(
        {
            "code": 404,
            "message": "User not found, please register and try again."
        }
    ), 404




if __name__ == "__main__":
    app.run(port="5004", debug=True)
