from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only
from flask_cors import CORS
from datetime import datetime
import os
from os import environ
from sqlalchemy import ForeignKey
from werkzeug.utils import secure_filename
import bcrypt


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/imatch'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

uploads_dir = os.path.join('assets/img/donations')

db = SQLAlchemy(app)
CORS(app)

# region MODELS
class User(db.Model):
    __tablename__ = 'user'
    
    username = db.Column(db.Integer, primary_key=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def json(self):
        return {"username": self.username, "password": self.password, "email": self.email}

class Item(db.Model):
    __tablename__ = 'item'

    itemID = db.Column(db.Integer, nullable=False, primary_key=True)
    itemName = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    itemImg = db.Column(db.String, nullable=False)

    def json(self):
        return {"itemID": self.itemID, "itemName": self.itemName, "category": self.category, "description": self.description, "itemImg": self.itemImg}

class Purchase(db.Model):
    __tablename__ = 'purchase'

    purchaseID = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String, nullable=False)
    itemID = db.Column(db.Integer, nullable=False)

    def json(self):
        return {"itemID": self.itemID, "itemName": self.itemName, "category": self.category, "description": self.description, "itemImg": self.itemImg}


#endregion


# region USER
@app.route("/registerUser", methods=['POST'])
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
    else:
        return jsonify(
            {
                "code": 404,
                "message": "User not found, please register and try again."
            }
        )
# endregion

# region CAROUSEL
# get all donation items
@app.route("/donation")
def getAllDonationItems():
    donationList = Donation.query.all()
    if len(donationList):
        itemList = []
        for donationItem in donationList:
            item = donationItem.json()
            formAnswers = getFormAnswersBySubmission(item["donationID"])
            itemDetails = getItem(item["itemID"]).get_json()["data"]
            itemDetails.pop("itemID")   # remove duplicate itemID

            itemList.append(dict(**item, **formAnswers, **itemDetails))
        return jsonify(
            {
                "code": 200,
                "data": {
                    "items": itemList
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no donations at the moment."
        }
    ), 404

# get specified donation item
@app.route("/donation/<string:donationID>")
def getDonationItem(donationID):
    donationItem = Donation.query.filter_by(donationID=donationID).first()
    if donationItem:
        formAnswers = getFormAnswersBySubmission(donationItem.donationID)
        itemDetails = getItem(donationItem.itemID).get_json()["data"]
        itemDetails.pop("itemID")   # remove duplicate itemID

        return jsonify(
            {
                "code": 200,
                "data": dict(**donationItem.json(), **formAnswers, **itemDetails)
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Donation does not exist."
        }
    ), 404

# API for search function
@app.route("/getItemsByCat/<string:cat>")
def getItemsByCategory(cat):
    catList = CategoryItem.query.filter_by(category=cat).all()
    catItemList = []
    for category in catList:
        itemList = Donation.query.filter_by(itemID=category.itemID).all()
        if (len(itemList)):
            categorydict = category.json()
            categorydict.pop("itemID")
            catList = [dict(**item.json(),**categorydict) for item in itemList]
            catItemList.extend(catList)
    if len(itemList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "itemsByCat": catItemList
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no items listed under this category."
        }
    ), 404

@app.route("/getItemsBySubCat/<subcat>")
def filterItems(subcat):
    subcatList = CategoryItem.query.filter_by(subCat=subcat).all()
    subcatItemList = []
    for category in subcatList:
        itemList = Donation.query.filter_by(itemID=category.itemID).all()
        if (len(itemList)):
            categorydict = category.json()
            categorydict.pop("itemID")
            subcatDetailsList = []
            for item in itemList:
                formAns = getFormAnswersBySubmission(item.donationID)
                subcatDetailsList.append(dict(**item.json(),**categorydict, **formAns))
            subcatItemList.extend(subcatDetailsList)
    if (len(subcatItemList)):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "items": subcatItemList
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no items donated under this Sub-category"
        }
    ), 404
    
# endregion

# region REQUEST
@app.route("/request/<string:contactNo>")
def getMwRequest(contactNo):
    itemReqList = Donation.query\
        .join(Request, Request.donationID==Donation.donationID)\
            .filter(Request.donationID==Donation.donationID)\
                .filter(Request.migrantID==contactNo)\
                    .distinct()

    itemIdArr = [id.json()['donationID'] for id in itemReqList]
    
    return jsonify(
        {
            "code": 200,
            "requestedItemIds": itemIdArr
        }
    )

@app.route("/request", methods=['POST'])
def addNewRequest():
        formData = request.form
        formDict = formData.to_dict()
        addtodb = {}
        addtodb["donationID"] = formDict['id']
        addtodb["deliveryLocation"] = formDict['destination']
        addtodb["migrantID"] = formDict['contact']

        # Get datetime of donation posting
        now = datetime.now()
        currentDT = now.strftime("%Y-%m-%d %H:%M:%S")
        timeSubmitted = currentDT

        addtodb["timeSubmitted"] = timeSubmitted

        item = Request(**addtodb)
        
        try:
            db.session.add(item)
            db.session.commit()
            return jsonify (
                {
                    "code": 200,
                    "message": "Request registered successfully!"
                }
            )
        except Exception as e:
            print(e)
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while registering your request, please try again later"
                }
            ), 500

# get all requests submitted by migrant workers
@app.route("/getRequests")
def getAllRequests():
    requestList = Request.query.all()
    data = []
    for request in requestList:
        row = {}
        donationID = request.donationID
        donationItem = Donation.query.filter_by(donationID=donationID).first()
        itemID = donationItem.itemID
        itemName = CategoryItem.query.filter_by(itemID=itemID).first().itemName
        row["itemName"] = itemName
        row.update(donationItem.json())
        row.update(request.json())
        row.pop('itemID')
        row.pop('donationID')
        data.append(row)
    columns = list(data[0].keys())
    if len(requestList):
        return jsonify(
            {
                "code": 200,
                "columnHeaders": columns,
                "data": data
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no requests at the moment."
        }
    ), 404

# get specific request by reqID
@app.route("/getRequests/<reqID>")
def getRequestByID(reqID):
    request = Request.query.filter_by(reqID=reqID).first()
    donationID = request.donationID
    donationItem = Donation.query.filter_by(donationID=donationID).first()
    itemID = donationItem.itemID
    itemName = CategoryItem.query.filter_by(itemID=itemID).first().itemName
    data = {}
    data["itemName"] = itemName
    data.update(request.json())
    data.update(donationItem.json())
    data.pop("itemID")
    data.pop("donationID")
    fieldNames = {}
    columns = sorted(list(data.keys()))
    for i in range(len(columns)):
        fieldNames[i] = columns[i]
    if request:
        return jsonify(
            {
                "code": 200,
                "columnHeaders": fieldNames,
                "data": data
                # "columnHeaders": NewRequest.metadata.tables["request"].columns.keys(),
                # "data": request
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Request cannot be found for this ID."
        }
    ), 404

# update request by reqID
@app.route("/updateRequest/<reqID>", methods=["PUT"])
def updateRequest(reqID):
    requested = Request.query.filter_by(reqID=reqID).first()
    donation = Donation.query.filter_by(donationID=requested.donationID).first()
    data = request.get_json()
    if (requested is None):
        return jsonify( 
            {
                "code": 404,
                "message": "This reqID is not found in the database."
            }
        )
    else:
        requested.deliveryLocation = data['deliveryLocation']
        # requested.requestQty = data['requestQty']
        requested.migrantID = data['migrantID']
        db.session.add(requested)
        db.session.commit()
        donation.itemStatus = data['itemStatus']
        db.session.add(donation)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Request successfully updated."
            }
        )

# delete request by reqID
@app.route("/deleteRequest/<reqID>", methods=["DELETE"])
def deleteRequest(reqID):
    request = Request.query.filter_by(reqID=reqID).first()
    try:
        db.session.delete(request)
        db.session.commit()
        return jsonify (
            {
                "code": 200,
                "message": "Row deleted successfully!"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while deleting the data, please try again later"
            }
        ), 500

# endregion


if __name__ == "__main__":
    app.run(port="5003", debug=True)
