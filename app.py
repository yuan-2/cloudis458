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

# region ITEMS
# get all items
@app.route("/items")
def getAllItems():
    itemList = Item.query.all()
    if len(itemList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "items": [item.json() for item in itemList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no items at the moment."
        }
    ), 404

# get specific item
@app.route("/item/<int:itemID>")
def getItem(itemID):
    item = Item.query.filter_by(itemID=itemID).first()
    if item:
        return jsonify(
            {
                "code": 200,
                "data": item.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Item does not exist."
        }
    ), 404
    
# endregion

# region PURCHASE
@app.route("/purchase/<int:purchaseID>")
def getPurchase(purchaseID):
    purchase = Purchase.query.filter_by(purchaseID=purchaseID).first()    
    return jsonify(
        {
            "code": 200,
            "data": purchase.json()
        }
    )

@app.route("/purchase", methods=['POST'])
def addPurchase():
        formData = request.form
        formDict = formData.to_dict()
        addtodb = {}
        addtodb["username"] = formDict['username']
        addtodb["itemID"] = formDict['itemID']
        item = Purchase(**addtodb)
        
        try:
            db.session.add(item)
            db.session.commit()
            return jsonify (
                {
                    "code": 200,
                    "message": "Purchased successfully!"
                }
            )
        except Exception as e:
            print(e)
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while purchasing, please try again later"
                }
            ), 500

# get all purchases submitted by user
@app.route("/purchases/<string:username>")
def getAllPurchases(username):
    userPurchases = Purchase.query.filter_by(username=username)
    if len(userPurchases) > 0:
        return jsonify(
            {
                "code": 200,
                "data": [purchase.json() for purchase in userPurchases]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no purchases at the moment."
        }
    ), 404

# get specific purchase by purchaseID
@app.route("/getPurchases/<int:purchaseID>")
def getPurchaseByID(purchaseID):
    purchase = Purchase.query.filter_by(purchaseID=purchaseID).first()
    if purchase:
        return jsonify(
            {
                "code": 200,
                "data": purchase.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Invalid purchase ID."
        }
    ), 404

# endregion


if __name__ == "__main__":
    app.run(port="5003", debug=True)
