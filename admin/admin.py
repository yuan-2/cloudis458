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

    id = db.Column(db.Integer, primary_key=True, nullable=False)
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

    def __init__(self, id, name, description, donorName, donorAddr, contactNo, category, quantity, requireDelivery, region, timeSubmitted, itemStatus):
        self.id = id
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

    def json(self):
        return {"id": self.id, "name": self.name, "description": self.description, "donorName": self.donorName, "donorAddr": self.donorAddr, 
                "contactNo": self.contactNo, "category": self.category, "quantity": self.quantity, "requireDelivery": self.requireDelivery, 
                "region": self.region, "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus}

# get all items submitted by donors where timeSubmitted > 0 and timeSubmitted <= 24 (time logic not done)
@app.route("/getAllItems")
def getAllItems():
    carouselList = CarouselItem.query.all()
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

# get specific wishlist submitted by migrant workers by wishlist ID
@app.route("/getItem/<int:id>")
def getItemByID(id):
    carouselItem = CarouselItem.query.filter_by(id=id).first()
    if carouselItem:
        return jsonify(
            {
                "code": 200,
                "data": carouselItem.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Item cannot be found for this ID."
        }
    ), 404

# edit donated (carousel) item in table
@app.route("/updateItem/<int:itemID>", methods=["PUT"])
def updateItem(itemID):
    item = CarouselItem.query.filter_by(id=itemID).first()
    data = request.get_json()
    if (item is None):
        return jsonify( 
            {
                "code": 404,
                "message": "This item ID is not found in the database."
            }
        )
    else:
        item.name = data['itemName']
        item.description = data['description']
        item.donorName = data['donorName']
        item.donorAddr = data['donorAddr']
        item.contactNo = data['contactNo']
        item.category = data['itemCategory']
        item.quantity = data['quantity']
        item.requireDelivery = data['requireDelivery']
        item.region = data['region']
        item.itemStatus = data['itemStatus']
        db.session.add(item)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Item successfully updated."
            }
        )


class Request(db.Model):
    __tablename__ = 'request'

    reqid = db.Column(db.Integer, primary_key=True, nullable=False)
    requestor = db.Column(db.String(50), nullable=False)
    deliveryLocation = db.Column(db.String(300), nullable=False)
    itemCategory = db.Column(db.String(50), nullable=False)
    requestQty = db.Column(db.String(50), nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)

    def __init__(self, reqid, requestor, deliveryLocation, itemCategory, requestQty, timeSubmitted):
        self.reqid = reqid
        self.requestor = requestor
        self.deliveryLocation = deliveryLocation
        self.itemCategory = itemCategory
        self.requestyQty = requestQty
        self.timeSubmitted = timeSubmitted

    def json(self):
        return {"reqid": self.reqid, "requestor": self.requestor, "deliveryLocation": self.deliveryLocation, "itemCategory": self.itemCategory, 
                "requestQty": self.requestQty, "timeSubmitted": self.timeSubmitted}

# get all requests submitted by migrant workers
@app.route("/getRequests")
def getAllRequests():
    requestList = Request.query.all()
    if len(requestList):
        return jsonify(
            {
                "code": 200,
                "data": [request.json() for request in requestList]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no requests at the moment."
        }
    ), 404

# get specific request submitted by migrant workers
@app.route("/getRequests/<int:id>")
def getRequestByID(id):
    request = Request.query.filter_by(reqid=id).first()
    if request:
        return jsonify(
            {
                "code": 200,
                "data": request.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Request cannot be found for this ID."
        }
    ), 404

# edit request in table
@app.route("/updateRequest/<int:id>", methods=["PUT"])
def updateRequest(id):
    requested = Request.query.filter_by(reqid=id).first()
    data = request.get_json()
    if (requested is None):
        return jsonify( 
            {
                "code": 404,
                "message": "This ID is not found in the database."
            }
        )
    else:
        requested.requestor = data['requestor']
        requested.deliveryLocation = data['deliveryLocation']
        requested.itemCategory = data['itemCategory']
        requested.requestQty = data['requestQty']
        db.session.add(requested)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Request successfully updated."
            }
        )


class Wishlist(db.Model):
    __tablename__ = 'wishlist'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    itemName = db.Column(db.String(50), nullable=False)
    remarks = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)
    itemStatus = db.Column(db.Integer, nullable=False)

    def __init__(self, id, itemName, remarks, category, timeSubmitted, itemStatus):
        self.id = id
        self.itemName = itemName
        self.remarks = remarks
        self.category = category
        self.timeSubmitted = timeSubmitted
        self.itemStauts = itemStatus

    def json(self):
        return {"id": self.id, "itemName": self.itemName, "remarks": self.remarks, "category": self.category, 
                "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus}

# get all requests submitted by migrant workers
@app.route("/getWishlist")
def getWishlist():
    wishlist = Wishlist.query.all()
    if len(wishlist):
        return jsonify(
            {
                "code": 200,
                "data": [wish.json() for wish in wishlist]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no requests at the moment."
        }
    ), 404

# get specific wishlist submitted by migrant workers by wishlist ID
@app.route("/getWishlist/<int:id>")
def getWishlistByID(id):
    wishlist = Wishlist.query.filter_by(id=id).first()
    if wishlist:
        return jsonify(
            {
                "code": 200,
                "data": wishlist.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Wishlist cannot be found for this ID."
        }
    ), 404

# edit wishlist in table
@app.route("/updateWishlist/<int:id>", methods=["PUT"])
def updateWishlist(id):
    wishlistItem = Wishlist.query.filter_by(id=id).first()
    data = request.get_json()
    if (wishlistItem is None):
        return jsonify( 
            {
                "code": 404,
                "message": "This ID is not found in the database."
            }
        )
    else:
        wishlistItem.itemName = data['itemName']
        wishlistItem.remarks = data['remarks']
        wishlistItem.category = data['itemCategory']
        wishlistItem.itemStatus = data['itemStatus']
        db.session.add(wishlistItem)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Wishlist successfully updated."
            }
        )


class Matches(db.Model):
    __tablename__ = 'matches'

    matchid = db.Column(db.Integer, primary_key=True, nullable=False)
    reqid = db.Column(db.Integer, nullable=False)
    requestorName = db.Column(db.String(50), nullable=False)
    requestorContactNo = db.Column(db.String(50), nullable=False)
    donorName = db.Column(db.String(50), nullable=False)
    donorContactNo = db.Column(db.String(50), nullable=False)
    requestedItem = db.Column(db.String(50), nullable=False)
    itemCategory = db.Column(db.String(50), nullable=False)
    dateSubmitted = db.Column(db.String(50), nullable=False)

    def __init__(self, matchid, reqid, requestorName, requestorContactNo, donorName, donorContactNo, requestedItem, itemCategory, dateSubmitted):
        self.matchid = matchid
        self.reqid = reqid
        self.requestorName = requestorName
        self.requestorContactNo = requestorContactNo
        self.donorName = donorName
        self.donorContactNo = donorContactNo
        self.requestedItem = requestedItem
        self.itemCategory = itemCategory
        self.dateSubmitted = dateSubmitted

    def json(self):
        return { "matchid": self.matchid, "reqid": self.reqid, "requestorName": self.requestorName, "requestorContactNo": self.requestorContactNo, "donorName": self.donorName, 
                "donorContactNo": self.donorContactNo, "requestedItem": self.requestedItem, "itemCategory": self.itemCategory, "dateSubmitted": self.dateSubmitted }

# get all successful matches
@app.route("/getSuccessfulMatches")
def getAllSuccessfulMatches():
    matches = Matches.query.all()
    if len(matches):
        return jsonify(
            {
                "code": 200,
                "data": [match.json() for match in matches]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no successful matches at the moment."
        }
    ), 404

# get specific successful match
@app.route("/getSuccessfulMatches/<int:id>")
def getSuccessfulMatch(id):
    match = Matches.query.filter_by(id=id).first()
    if match:
        return jsonify(
            {
                "code": 200,
                "data": { match.json() }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no successful matches at the moment."
        }
    ), 404


if __name__ == "__main__":
    app.run(port="5000", debug=True)
