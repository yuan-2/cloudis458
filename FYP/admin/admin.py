from distutils.command.upload import upload
from urllib import response
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func

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

uploads_dir = os.path.join('../assets/img/donations')


class CarouselItem(db.Model):
    __tablename__ = 'carousel'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
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
    itemStatus = db.Column(db.Integer, nullable=False)
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
        return {"id": self.id, "itemName": self.itemName, "description": self.description, "donorName": self.donorName, "donorAddr": self.donorAddr, 
                "contactNo": self.contactNo, "category": self.category, "quantity": self.quantity, "requireDelivery": self.requireDelivery, 
                "region": self.region, "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus, "fileName": self.fileName}

# get column headers
@app.route("/getCarouselItemColumns")
def getCarouselItemColumns():
    return jsonify(
        {
            "code": 200,
            "data": {
                "columns": CarouselItem.metadata.tables["carousel"].columns.keys()
            }
        }
    )

# get all items submitted by donors where timeSubmitted > 0 and timeSubmitted <= 24 (time logic not done)
@app.route("/getAllItems")
def getAllItems():
    carouselList = CarouselItem.query.all()
    if len(carouselList):
        # result = []
        # columnNames = dir(CarouselItem)
        # print(type(columnNames))
        # for item in carouselList:
        #     for colName in columnNames:
        #         result.append({ colName: item[colName] })
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

# get specific item in carousel
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
        # for col in data:
        #     item.col = data[col]
        item.itemName = data['itemName']
        item.description = data['description']
        item.donorName = data['donorName']
        item.donorAddr = data['donorAddr']
        item.contactNo = data['contactNo']
        item.category = data['category']
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

# edit donated (carousel) photo in table
@app.route("/updatePhoto/<int:itemID>", methods=["POST"])
def updatePhoto(itemID):
    item = CarouselItem.query.filter_by(id=itemID).first()
    data = request.to_dict()
    if (item is None):
        return jsonify( 
            {
                "code": 404,
                "message": "This item ID is not found in the database."
            }
        )
    else:
        imgFile = request.files['file']
        fileName = secure_filename(imgFile.filename)
        imgFile.save(os.path.join(uploads_dir, fileName))
        item.fileName = data['itemImg']
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
    requestorContactNo = db.Column(db.String(50), nullable=False)
    deliveryLocation = db.Column(db.String(300), nullable=False)
    itemCategory = db.Column(db.String(50), nullable=False)
    requestQty = db.Column(db.String(50), nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)

    def __init__(self, reqid, requestorContactNo, deliveryLocation, itemCategory, requestQty, timeSubmitted):
        self.reqid = reqid
        self.requestorContactNo = requestorContactNo
        self.deliveryLocation = deliveryLocation
        self.itemCategory = itemCategory
        self.requestyQty = requestQty
        self.timeSubmitted = timeSubmitted

    def json(self):
        return {"reqid": self.reqid, "requestorContactNo": self.requestorContactNo, "deliveryLocation": self.deliveryLocation, "itemCategory": self.itemCategory, 
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

# get requests submitted for specific item
@app.route("/getRequests/<item>")
def getRequestByItem(item):
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
        wishlistItem.category = data['category']
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
    requestorContactNo = db.Column(db.String(50), nullable=False)
    donorName = db.Column(db.String(50), nullable=False)
    donorContactNo = db.Column(db.String(50), nullable=False)
    requestedItem = db.Column(db.String(50), nullable=False)
    itemCategory = db.Column(db.String(50), nullable=False)
    dateSubmitted = db.Column(db.String(50), nullable=False)

    def __init__(self, matchid, reqid, requestorContactNo, donorName, donorContactNo, requestedItem, itemCategory, dateSubmitted):
        self.matchid = matchid
        self.reqid = reqid
        self.requestorContactNo = requestorContactNo
        self.donorName = donorName
        self.donorContactNo = donorContactNo
        self.requestedItem = requestedItem
        self.itemCategory = itemCategory
        self.dateSubmitted = dateSubmitted

    def json(self):
        return { "matchid": self.matchid, "reqid": self.reqid, "requestorContactNo": self.requestorContactNo, "donorName": self.donorName, 
                "donorContactNo": self.donorContactNo, "requestedItem": self.requestedItem, "itemCategory": self.itemCategory, "dateSubmitted": self.dateSubmitted }

# get column headers
# @app.route("/getSuccessMatchColHeaders")
# def getSuccessfulMatchesColumnHeaders():
#     return jsonify(
#         {
#             "code": 200,
#             "data": {
#                 "columns": Matches.metadata.tables["carousel"].columns.keys()
#             }
#         }
#     )


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
    match = Matches.query.filter_by(reqid=id).first()
    if match:
        return jsonify(
            {
                "code": 200,
                "data": match.json() 
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no successful matches at the moment."
        }
    ), 404

# edit wishlist in table
@app.route("/updateSuccessfulMatches/<int:id>", methods=["PUT"])
def updateSuccessfulMatches(id):
    match = Matches.query.filter_by(reqid=id).first()
    data = request.get_json()
    if (match is None):
        return jsonify( 
            {
                "code": 404,
                "message": "This ReqID is not found in the database."
            }
        )
    else:
        match.reqid = data['reqid']
        match.requestorContactNo = data['requestorContactNo']
        match.donorName = data['donorName']
        match.donorContactNo = data['donorContactNo']
        match.requestedItem = data['requestedItem']
        match.itemCategory = data['itemCategory']
        db.session.add(match)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Match successfully updated."
            }
        )


# get consolidated criteria of migrant worker
@app.route("/getCriteria/<migrantworker>")
def getMigrantWorkerCriteria(migrantworker):
    # get total no. of successful matches for specific migrant worker
    successMatchCount = Matches.query.filter_by(requestorContactNo=migrantworker).count()
    failMatchCount = Request.query.filter_by(requestor=migrantworker).count() - successMatchCount
    # Matches.query.with_entities(Matches.requestorContactNo, func.count(Matches.requestorContactNo)).group_by(Matches.requestorContactNo).all()
    if successMatchCount and failMatchCount:
        return jsonify(
            {
                "code": 200,
                "data": { 
                    "successMatchCount": successMatchCount, 
                    "failMatchCount": failMatchCount
                }
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
