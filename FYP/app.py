from cgi import print_directory
from cv2 import Mat_DEPTH_MASK
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
    userType = db.Column(db.String(20), nullable=False)

    def __init__(self, username, password, userType):
        self.username = username
        self.password = password
        self.userType = userType

    def json(self):
        return {"username": self.username, "password": self.password, "userType": self.userType}

class FormBuilder(db.Model):
    __tablename__ = 'formbuilder'

    fieldID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    formName = db.Column(db.String(15), nullable=False)
    fieldName = db.Column(db.String(50), nullable=False)
    fieldType = db.Column(db.String(15), nullable=False)
    placeholder = db.Column(db.String(50))
    options = db.Column(db.String(200))


    def json(self):
        return {"fieldID": self.fieldID, "formName": self.formName, "fieldName": self.fieldName, "fieldType": self.fieldType, "placeholder": self.placeholder, "options": self.options}

class CategoryItem(db.Model):
    __tablename__ = 'categoryitem'

    itemID = db.Column(db.Integer, nullable=False, primary_key=True)
    itemName = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    subCat = db.Column(db.String, nullable=False)


    def json(self):
        return {"itemID": self.itemID, "itemName": self.itemName, "category": self.category, "subCat": self.subCat}

class Donation(db.Model):
    __tablename__ = 'donation'
    
    donorID = db.Column(db.Integer)
    donationID = db.Column(db.String(30), nullable=False, primary_key=True)
    itemID = db.Column(db.Integer, nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)
    itemStatus = db.Column(db.String(50), nullable=False)
        
    def json(self):
        return {"donationID": self.donationID, "donorID": self.donorID, "donationID": self.donationID, "itemID": self.itemID, "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus}

class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    
    migrantID = db.Column(db.Integer)
    wishlistID = db.Column(db.String(30), nullable=False, primary_key=True)
    itemID = db.Column(db.Integer, nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)
    itemStatus = db.Column(db.String(50), nullable=False)
        
    def json(self):
        return {"wishlistID": self.wishlistID, "migrantID": self.migrantID, "wishlistID": self.wishlistID, "itemID": self.itemID, "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus}

class FormAnswers(db.Model):
    __tablename__ = 'formanswers'

    answerID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    submissionID = db.Column(db.String(30), nullable=False)
    # , db.ForeignKey(Learner.empID)
    formName = db.Column(db.String(15), nullable=False)
    fieldID = db.Column(db.Integer, nullable=False)
    answer = db.Column(db.String(50), nullable=False)

    def json(self):
        return {"answerID": self.answerID, "submissionID": self.submissionID, "fieldID": self.fieldID, "formName": self.formName, "answer": self.answer}

class Request(db.Model):
    __tablename__ = 'request'
    
    reqID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    migrantID = db.Column(db.Integer, nullable=False)           #, ForeignKey('user.username')
    deliveryLocation = db.Column(db.Integer, nullable=False)
    donationID = db.Column(db.String(30), nullable=False)       #, ForeignKey('donation.id')
    timeSubmitted = db.Column(db.Date, nullable=False)
        
    def json(self):
        return {"reqID": self.reqID, "migrantID": self.migrantID, "deliveryLocation": self.deliveryLocation, "donationID": self.donationID, "timeSubmitted": self.timeSubmitted}

class Matches(db.Model):
    __tablename__ = 'matches'

    matchID = db.Column(db.Integer, primary_key=True, nullable=False)
    reqID = db.Column(db.Integer, nullable=False)
    migrantID = db.Column(db.Integer, nullable=False)
    donorID = db.Column(db.Integer, nullable=False)
    matchDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # def __init__(self, matchID, reqID, migrantID, donorID, matchDate):
    #     self.matchID = matchID
    #     self.reqID = reqID
    #     self.migrantID = migrantID
    #     self.donorID = donorID
    #     self.matchDate = matchDate

    def json(self):
        return { "matchID": self.matchID, "reqID": self.reqID, "migrantID": self.migrantID, 
                "donorID": self.donorID, "matchDate": self.matchDate }

class Faq(db.Model):
    __tablename__ = 'faq'

    faqID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    question = db.Column(db.String(300), nullable=False)
    answer = db.Column(db.String(300), nullable=False)
    section = db.Column(db.String(10), nullable=False)

    def __init__(self, faqID, question, answer, section):
        self.faqID = faqID
        self.question = question
        self.answer = answer
        self.section = section

    def json(self):
        return {"faqID": self.faqID, "question": self.question, "answer": self.answer, "section": self.section}

#endregion


# region USER
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

# region FORMBUILDER
# get all fields by form
@app.route("/formbuilder/<string:formName>")
def getFieldsByForm(formName):
    fieldlist = FormBuilder.query.filter_by(formName=formName).all()
    if len(fieldlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "items": [field.json() for field in fieldlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no fields for the current form."
        }
    ), 404

# get specific field
@app.route("/formbuilder/<int:fieldID>")
def getField(fieldID):
    field = FormBuilder.query.filter_by(fieldID=fieldID).first()
    if field:
        return jsonify(
            {
                "code": 200,
                "data":  field.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No field was found."
        }
    ), 404

# create new field
@app.route('/formbuilder', methods=['POST'])
def createField():
    data = request.get_json()
    item = FormBuilder(**data)
    if ( request.get_json() is not None ): 
        try:
            db.session.add(item)
            db.session.commit()
            return jsonify(item.json()), 201
        except Exception:
            return jsonify({
                "message": "Unable to commit to database."
            }), 500

# edit existing faq
@app.route('/formbuilder/<int:fieldID>', methods=['POST'])
def edit_field(fieldID):
    data = request.get_json()
    item = FormBuilder.query.filter_by(fieldID=fieldID).first()
    if ( item is not None ): 
        try:
            item.fieldName = data['fieldName']
            item.fieldType = data['fieldType']
            if 'placeholder' in data:
                item.placeholder = data['placeholder']
            if 'options' in data:
                item.options = data['options']
            db.session.commit()
            return jsonify(item.json()), 201
        except Exception:
            return jsonify({
                "message": "Unable to commit to database."
            }), 500

# delete existing field
@app.route('/formbuilder/<int:fieldID>', methods=["DELETE"])
def delete_field(fieldID):
    item = FormBuilder.query.filter_by(fieldID=fieldID).first()
    ansList = FormAnswers.query.filter_by(fieldID=fieldID).all()
    if ( item is not None ): 
        try:
            # delete answers linked to field
            for ans in ansList:
                db.session.delete(ans)

            # delete field
            db.session.delete(item)
            db.session.commit()
            return jsonify(item.json()), 201
        except Exception as e:
            print(e)
            return jsonify({
                "message": "Unable to commit to database."
            }), 500
#endregion

# region CATEGORYITEMS
@app.route("/getCatalog")
def retrieveCatalog():
    catalog = CategoryItem.query.all()
    
    if (catalog):
        return jsonify(
            {
                "code": 200,
                "items": [catalogitem.json() for catalogitem in catalog]
            }
        )
    else:
        return jsonify(
            {
                "code": 404,
                "message": "Catalog seems to be empty or the API file is not running"
            }
        )

# get all existing categories to be displayed in drop down fields
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

# get all existing subcategories to be displayed in drop down fields
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

@app.route("/getItemById/<int:itemID>")
def getItem(itemID):
    item = CategoryItem.query.filter_by(itemID=itemID).first()
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
            "message": "No item was found."
        }
    ), 404
#endregion

# region FORMANSWERS + CAROUSEL/WISHLIST
# get all form answers by donation/wishlist submission
def getFormAnswersBySubmission(submissionID):
    answerlist = FormAnswers.query.filter_by(submissionID=submissionID).all()

    # map answers to field names
    mappedAnswerlist = {}
    for answer in answerlist:
        field = FormBuilder.query.filter_by(fieldID=answer.fieldID).options(load_only('fieldName')).first()
        mappedAnswerlist[field.fieldName] = answer.answer
    
    return mappedAnswerlist

# get all details of a donation/wishlist submission
@app.route("/formanswers/<string:submissionID>")
def getAllDetailsBySubmission(submissionID):
    # check if submission from Donation or wishlist
    submission = Donation.query.filter_by(donationID=submissionID).first()
    if submission is None:
        submission = Wishlist.query.filter_by(wishlistID=submissionID).first()

    if submission is not None:
        formAnswersList = getFormAnswersBySubmission(submissionID)

        return jsonify(
            {
                "code": 200,
                "data": dict(**submission.json(), **formAnswersList)
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No submission was found."
        }
    ), 404

# create new submission
@app.route('/formanswers', methods=['POST'])
def createSubmission():
    formData = request.form
    formDict = formData.to_dict()
    files = request.files
    userid = formDict['contactNo']
    formName =  formDict['formName']
    itemID = formDict['itemNameOptions']

    # calculate submissionID (datetime userID)
    now = datetime.now()
    currentDT = now.strftime("%Y-%m-%d %H:%M:%S")
    submissionID = currentDT + " " + userid
    # print(submissionID)

    # file uploading
    for fileId in files:
        file = files[fileId]
        # save file
        fileName = secure_filename(file.filename)
        file.save(os.path.join(uploads_dir, fileName))

    # for answer in formDict:
    #     print(type(answer))
    #     print(answer + ": " +formDict[answer])

    # submit into donation/wishlist
    details = {"itemID": itemID, "timeSubmitted": currentDT, "itemStatus": "Available"}
    if formName == "wishlist":
        details["migrantID"] = userid
        details["wishlistID"] = submissionID
        submission = Wishlist(**details)
        try:
                db.session.add(submission)
                db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({
                "message": "Unable to commit to database.",
                "data" : submission.json()
            }), 500
    elif formName == "donation":
        details["donorID"] = userid
        details["donationID"] = submissionID
        submission = Donation(**details)
        try:
                db.session.add(submission)
                db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({
                "message": "Unable to commit to database.",
                "data" : submission.json()
            }), 500

    # submit into formAnswers
    for id in formDict:
        answer = {"submissionID": submissionID, "formName": formName, "fieldID": id, "answer": formDict[id]}
        item = FormAnswers(**answer)
        if ( id.isdigit() ): 
            try:
                db.session.add(item)
                db.session.commit()
            except Exception as e:
                print(e)
                return jsonify({
                    "message": "Unable to commit to database.",
                    "data" : item.json()
                }), 500
    
    return jsonify(formDict), 201

# get all form answers for any form
@app.route("/getFormAnswers/<formName>")
def getFormAnswers(formName):
    formFields = FormBuilder.query.filter_by(formName=formName)
    if formName == "donation":
        tableFields = Donation.metadata.tables["donation"].columns.keys()
    elif formName == "wishlist":
        tableFields = Wishlist.metadata.tables["wishlist"].columns.keys()
    fieldNames = {}
    for field in formFields:
        fieldNames[field.fieldID] = field.fieldName
    for field in tableFields:
        lastKey = list(fieldNames.keys())[-1]
        if field == "itemID":
            fieldNames[lastKey + 1] = "itemName"
        else:
            fieldNames[lastKey + 1] = field
    data = []
    if formName == "donation":
        submissionIDList = Donation.query.with_entities(Donation.donationID).distinct()
    elif formName == "wishlist":
        submissionIDList = Wishlist.query.with_entities(Wishlist.wishlistID).distinct()
    for subID in submissionIDList:
        row = {}
        if formName == "donation":
            submission = Donation.query.filter_by(donationID=subID[0]).first().json()
        elif formName == "wishlist":
            submission = Wishlist.query.filter_by(wishlistID=subID[0]).first().json()
        row.update(submission)
        itemID = row['itemID']
        row["itemName"] = CategoryItem.query.filter_by(itemID=itemID).first().itemName
        row.pop("itemID")
        formAnswers = FormAnswers.query.filter_by(formName=formName).filter_by(submissionID=subID[0])
        ansFields = []
        for ans in formAnswers:
            ansFields.append(ans.fieldID)
            row[fieldNames[ans.fieldID]] = ans.answer
        if len(ansFields) < len(fieldNames):
            remainder = len(fieldNames) - len(ansFields)
            fieldIDList = list(fieldNames.keys())
            for i in range(1, remainder + 1):
                if fieldNames[fieldIDList[-i]] not in row.keys():
                    row[fieldNames[fieldIDList[-i]]] = ""
        data.append(row)
    if len(data) > 0:
        return jsonify( 
            {
                "code": 200,
                "columnHeaders": fieldNames,
                "data": data
            }
        )
    else:
        return jsonify( 
            {
                "code": 404,
                "message": "No form answers can be found for this form."
            }
        )

# get all form answers for specific forms (donation & wishlist items)
@app.route("/getFormAnswers/<formName>/<submissionID>")
def getSpecificFormAnswers(formName, submissionID):
    formAnswers = FormAnswers.query.filter_by(submissionID=submissionID)
    formFields = FormBuilder.query.filter_by(formName=formName)
    if formName == "donation":
        tableFields = Donation.metadata.tables["donation"].columns.keys()
    elif formName == "wishlist":
        tableFields = Wishlist.metadata.tables["wishlist"].columns.keys()
    fieldNames = {}
    for field in formFields:
        fieldNames[field.fieldID] = field.fieldName
    for field in tableFields:
        fieldNames[len(fieldNames) + 1] = field
    data = {}
    for ans in formAnswers:
        data["submissionID"] = submissionID
        data[fieldNames[ans.fieldID]] = ans.answer
        if formName == "donation":
            item = Donation.query.filter_by(donationID=submissionID).first()
        elif formName == "wishlist":
            item = Wishlist.query.filter_by(wishlistID=submissionID).first()
        data.update(item.json())
        # data.pop('itemName')
    # data.pop('timeSubmitted')
    # data.pop('itemID')
    if len(data) > 0:
        return jsonify( 
            {
                "code": 200,
                "columnHeaders": fieldNames,
                "data": data
            }
        )
    else:
        return jsonify( 
            {
                "code": 404,
                "message": "No form answers can be found for this submission ID."
            }
        )

# edit donated (donation) item OR wishlist in table
@app.route("/updateFormAnswers/<formName>/<submissionID>", methods=["PUT"])
def updateFormAnswers(formName, submissionID):
    formAnswers = FormAnswers.query.filter_by(submissionID=submissionID)
    formFields = FormBuilder.query.filter_by(formName=formName)
    if formName == "donation":
        otherFormFields = Donation.query.filter_by(donationID=submissionID).first()
    elif formName == "wishlist":
        otherFormFields = Wishlist.query.filter_by(wishlistID=submissionID).first()
    fieldNames = {}
    for field in formFields:
        fieldNames[field.fieldID] = field.fieldName
    data = request.get_json()
    if (formAnswers is None):
        return jsonify( 
            {
                "code": 404,
                "message": "There is no submission for this submission ID in the database."
            }
        )
    else:
        dataDict = {}
        if formName == "donation":
            otherFormFields.donorID = data["donorID"]
            otherFormFields.donationID = data["donationID"]
        elif formName == "wishlist":
            otherFormFields.wishlistID = data["wishlistID"]
            otherFormFields.migrantID = data["migrantID"]
        # otherFormFields.submissionID = data["submissionID"]
        # otherFormFields.itemName = data["itemName"]
        # otherFormFields.itemCategory = data["itemCategory"]
        otherFormFields.itemStatus = data["itemStatus"]
        db.session.add(otherFormFields)
        db.session.commit()
        for d in data:
            if d not in ["donorID", "carouselID", "wishlistID", "migrantID", "itemStatus"]:
                dataDict[d] = data[d]
        for ans in formAnswers:
            fieldName = FormBuilder.query.filter_by(fieldID=ans.fieldID).first().fieldName
            if ans.fieldID != 3:
                fieldName = FormBuilder.query.filter_by(fieldID=ans.fieldID).first().fieldName
                ans.answer = dataDict[fieldName]
                dataDict.pop(fieldName)
                db.session.add(ans)
                db.session.commit()
        for data in dataDict:
            if data.isdigit() == False:
                answer = {"submissionID": submissionID, "formName": formName, "fieldID": FormBuilder.query.filter_by(fieldName=data).first().fieldID, "answer": dataDict[data]}
                answer = FormAnswers(**answer)
                db.session.add(answer)
                db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Data successfully updated.",
                "formAns": [ans.json() for ans in formAnswers],
                "otherFormFields": otherFormFields.json()
            }
        )

# edit uploaded photo
@app.route("/updatePhoto/<submissionID>", methods=['POST'])
def updatePhoto(submissionID):
    formData = request.form
    formDict = formData.to_dict()
    imgFile = request.files['file']
    formField = FormBuilder.query.filter_by(formName="carousel").filter_by(fieldName="Item Photo").first()
    fieldID = formField.fieldID
    formAnswer = FormAnswers.query.filter_by(submissionID=submissionID).filter_by(fieldID=fieldID).first()
    # save file
    fileName = secure_filename(imgFile.filename.replace(" ", ""))
    # print(formDict)
    imgFile.save(os.path.join(uploads_dir, fileName))
    # os.open(uploads_dir+secure_filename(fileName), os.O_RDWR | os.O_CREAT, 0o666)
    file = formDict['itemImg']

    # delete old photo file
    oldFile = formAnswer.answer
    os.remove(os.path.join(uploads_dir, oldFile))
    
    try:
        formAnswer.answer = file
        db.session.add(formAnswer)
        db.session.commit()
        return jsonify (
            {
                "code": 200,
                "message": "Photo Successfully Updated"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while updating the item photo, please try again later"
            }
        ), 500

# delete formAnswers + carousel/wishlist
@app.route("/deleteRow/<formName>/<submissionID>", methods=["DELETE"])
def deleteRow(formName, submissionID):
    if formName == "carousel":
        row = Carousel.query.filter_by(carouselID=submissionID).first()
        oldFile = FormAnswers.query.filter_by(submissionID=submissionID).filter_by(fieldID=3).first().answer
    elif formName == "wishlist":
        row = Wishlist.query.filter_by(wishlistID=submissionID).first()
    formAnswers = FormAnswers.query.filter_by(submissionID=submissionID)
    try:
        if formName == "carousel":
            os.remove(os.path.join(uploads_dir, oldFile))
        db.session.delete(row)
        db.session.commit()
        for ans in formAnswers:
            db.session.delete(ans)
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

# region WISHLIST
# get all items in wishlist
@app.route("/wishlist")
def getAllWishListItems():
    wishList = Wishlist.query.all()
    if len(wishList):
        itemList = []
        for wishlistItem in wishList:
            item = wishlistItem.json()
            formAnswers = getFormAnswersBySubmission(item["wishlistID"])
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
            "message": "Wishlist is currently empty."
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

# region MATCHES
# get all successful matches 
@app.route("/getSuccessfulMatches")
def getAllSuccessfulMatches():
    matches = Matches.query.all()
    data = []
    for match in matches:
        row = {}
        reqID = match.reqID
        request = Request.query.filter_by(reqID=reqID).first()
        donationID = request.donationID
        donationItem = Donation.query.filter_by(donationID=donationID).first()
        itemID = donationItem.itemID
        itemName = CategoryItem.query.filter_by(itemID=itemID).first().itemName
        row["itemName"] = itemName
        row.update(match.json())
        row.update(request.json())
        row.update(donationItem.json())
        row.pop('donationID')
        row.pop('reqID')
        row.pop('itemID')
        data.append(row)
    columns = list(data[0].keys())
    if len(matches):
        return jsonify(
            {
                "code": 200,
                "columnHeaders": columns,
                "data": data
                # "data": [match.json() for match in matches], 
                # "columnHeaders": Matches.metadata.tables["matches"].columns.keys()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no successful matches at the moment."
        }
    ), 404

# get specific successful match 
@app.route("/getSuccessfulMatches/<matchID>")
def getSuccessfulMatch(matchID):
    data = {}
    match = Matches.query.filter_by(matchID=matchID).first()
    reqID = match.reqID
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
    data.pop("reqID")
    columns = list(data.keys())
    if match:
        return jsonify(
            {
                "code": 200,
                "columnHeaders": columns,
                "data": data
                # "columnHeaders": Matches.metadata.tables["matches"].columns.keys(),
                # "data": match
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no successful matches at the moment."
        }
    ), 404

# edit SuccessfulMatch in table
@app.route("/updateSuccessfulMatches/<matchID>", methods=["PUT"])
def updateSuccessfulMatches(matchID):
    match = Matches.query.filter_by(matchID=matchID).first()
    reqID = match.reqID
    req = Request.query.filter_by(reqID=reqID).first()
    donationID = req.donationID
    donationItem = Donation.query.filter_by(donationID=donationID).first()
    data = request.get_json()
    print(data)
    if (match is None):
        return jsonify( 
            {
                "code": 404,
                "message": "This matchID is not found in the database."
            }
        )
    else:
        match.donorID = data['donorID']
        db.session.add(match)
        db.session.commit()
        req.deliveryLocation = data['deliveryLocation']
        req.requestQty = data['requestQty']
        db.session.add(req)
        db.session.commit()
        donationItem.itemStatus = data['itemStatus']
        donationItem.donorID = data['donorID']
        db.session.add(donationItem)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Match successfully updated.",
                "match": match.json(),
                "data": data,
                "olddata": data
            }
        )

# add new match
@app.route("/addMatch", methods=['POST'])
def addNewMatch():
        formData = request.form
        formDict = formData.to_dict()
        addtodb = {}
        addtodb["reqID"] = formDict['reqID']
        addtodb["migrantID"] = formDict['migrantID']
        addtodb["donorID"] = formDict['donorID']

        # Get datetime of donation posting
        now = datetime.now()
        currentDT = now.strftime("%Y-%m-%d %H:%M:%S")
        timeSubmitted = currentDT

        addtodb["matchDate"] = timeSubmitted
        print(addtodb)
        item = Matches(**addtodb)
        
        try:
            db.session.add(item)
            db.session.commit()
            return jsonify (
                {
                    "code": 200,
                    "message": "Match added successfully!"
                }
            )
        except Exception as e:
            print(e)
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while adding your match, please try again later"
                }
            ), 500

# delete match by matchID
@app.route("/deleteMatch/<matchID>", methods=["DELETE"])
def deleteMatch(matchID):
    match = Matches.query.filter_by(matchID=matchID).first()
    try:
        db.session.delete(match)
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

# rank migrant workers according to reqHistory, get list of MWs who are prioritised
@app.route("/getRankByReqHistory/<donationID>")
def getRankByReqHistory(donationID):
    requests = Request.query.filter_by(donationID=donationID)
    if requests:
        reqHist = {}
        for req in requests:
            migrantWorkerCount = Matches.query.filter_by(migrantID=req.migrantID).count()
            if migrantWorkerCount in reqHist.keys():
                reqHist[migrantWorkerCount] += [req.migrantID]
            else:
                reqHist[migrantWorkerCount] = [req.migrantID]
        allKeys = reqHist.keys()
        minValue = min(allKeys, default="EMPTY")
        priorityMW = reqHist[minValue]
        mwPoints = {}
        # check whether item requires delivery
        deliveryFieldID = FormBuilder.query.filter_by(fieldName="Delivery Method").first()
        deliveryOption = FormAnswers.query.filter_by(submissionID=donationID).filter_by(fieldID=deliveryFieldID).first()
        # if deliveryOption == "Self Pick-Up":
            # find migrant worker(s) w shortest distance 
        
        # else: 
        # check for the list of MWs, how long since each of them have gotten an item
        # i only wrote down the logic... the code below doesn't work yet HAHAHA
        if minValue != 0:      
            timeNow = datetime.now()
            for mwNum in priorityMW:
                mw = Matches.query.filter_by(migrantID=mwNum).first()
                lastItemTime = mw.matchDate
                days = timeNow - lastItemTime # convert difference into no. of days
                if 0 <= days < 14:
                    mwPoints[mwNum] = 0
                elif 14 <= days < 28:
                    mwPoints[mwNum] = 1
                elif 28 <= days < 42:
                    mwPoints[mwNum] = 2
                elif 42 <= days < 56:
                    mwPoints[mwNum] = 4
                else:
                    mwPoints[mwNum] = 6
            # if mw.lastItemTime in lastItem.keys():
            #     lastItem[mw.lastItemTime] += [mw.contactNo]
            # else:
            #     lastItem[mw.lastItemTime] = [mw.contactNo]
        # allKeys = lastItem.keys()
        # minValue = min(allKeys)
        # priorityMW = lastItem[minValue]
        return jsonify(
            {
                "code": 200,
                "data": priorityMW
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No migrant workers requested for this item ID."
        }
    ), 404

# endregion

# region FAQ
# get all FAQs
@app.route("/faq")
def getAllFaq():
    faqlist = Faq.query.all()
    if len(faqlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "items": [faq.json() for faq in faqlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no FAQs at the moment."
        }
    ), 404

# get specific faq
@app.route("/faq/<int:faqID>")
def getFaq(faqID):
    faq = Faq.query.filter_by(faqID=faqID).first()
    if faq:
        return jsonify(
            {
                "code": 200,
                "data":  faq.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No FAQ was found."
        }
    ), 404

# create new faq
@app.route('/faq', methods=['POST'])
def create_faq():
    data = request.get_json()
    item = Faq(None, **data)
    if ( request.get_json() is not None ): 
        try:
            db.session.add(item)
            db.session.commit()
            return jsonify(item.json()), 201
        except Exception:
            return jsonify({
                "message": "Unable to commit to database."
            }), 500

# edit existing faq
@app.route('/faq/<int:faqID>', methods=['POST'])
def edit_faq(faqID):
    data = request.get_json()
    item = Faq.query.filter_by(faqID=faqID).first()
    if ( item is not None ): 
        try:
            item.question = data['question']
            item.answer = data['answer']
            item.section = data['section']
            db.session.commit()
            return jsonify(item.json()), 201
        except Exception:
            return jsonify({
                "message": "Unable to commit to database."
            }), 500

# delete existing faq
@app.route('/faq/<int:faqID>', methods=["DELETE"])
def delete_faq(faqID):
    item = Faq.query.filter_by(faqID=faqID).first()
    if ( item is not None ): 
        try:
            db.session.delete(item)
            db.session.commit()
            return jsonify(item.json()), 201
        except Exception:
            return jsonify({
                "message": "Unable to commit to database."
            }), 500

# endregion

if __name__ == "__main__":
    app.run(port="5003", debug=True)
