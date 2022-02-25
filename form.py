from ast import For
from fileinput import filename
from re import sub
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only
from flask_cors import CORS
from datetime import datetime
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/fyptest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

uploads_dir = os.path.join('assets/img/donations')

db = SQLAlchemy(app)
CORS(app)

#region MODELS
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

class Carousel(db.Model):
    __tablename__ = 'newcarousel'
    
    donorID = db.Column(db.Integer)
    carouselID = db.Column(db.String(30), nullable=False, primary_key=True)
    itemID = db.Column(db.Integer, nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)
    itemStatus = db.Column(db.String(50), nullable=False)
        
    def json(self):
        return {"carouselID": self.carouselID, "donorID": self.donorID, "carouselID": self.carouselID, "itemID": self.itemID, "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus}

class Wishlist(db.Model):
    __tablename__ = 'newwishlist'
    
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
#endregion


#region FORMBUILDER
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

#region CATEGORYITEMS
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

# FORMANSWERS + CAROUSEL/WISHLIST
# get all form answers by carousel/wishlist submission
def getFormAnswersBySubmission(submissionID):
    answerlist = FormAnswers.query.filter_by(submissionID=submissionID).all()

    # map answers to field names
    mappedAnswerlist = {}
    for answer in answerlist:
        field = FormBuilder.query.filter_by(fieldID=answer.fieldID).options(load_only('fieldName')).first()
        mappedAnswerlist[field.fieldName] = answer.answer
    
    return mappedAnswerlist

# get all details of a carousel/wishlist submission
@app.route("/formanswers/<string:submissionID>")
def getAllDetailsBySubmission(submissionID):
    # check if submission from Carousel or wishlist
    submission = Carousel.query.filter_by(carouselID=submissionID).first()
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
    itemName = formDict['itemNameOptions']
    itemCategory = formDict['itemCategoryOptions']

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

    # submit into carousel/wishlist
    details = {"submissionID": submissionID, "itemName": itemName, "itemCategory": itemCategory, "timeSubmitted": currentDT, "itemStatus": "Available"}
    if formName == "request":
        details["migrantID"] = userid
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
    elif formName == "donate":
        details["donorID"] = userid
        submission = Carousel(**details)
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

# CAROUSEL
# get all carousel items
@app.route("/carousel")
def getAllCarouselItems():
    carouselList = Carousel.query.all()
    if len(carouselList):
        itemList = []
        for carouselItem in carouselList:
            item = carouselItem.json()
            formAnswers = getFormAnswersBySubmission(item["carouselID"])
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

# API for search function
@app.route("/getItemsByCat/<string:cat>")
def getItemsByCategory(cat):
    categoryList = Carousel.query.with_entities(Carousel.itemID).distinct()
    itemList = []
    for category in categoryList:
        item = CategoryItem.query.filter_by(itemID=category,category=cat).first()
        if item is not None:
            itemList.append(item)
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

@app.route("/getItemsBySubCat/<subcat>")
def filterItems(subcat):
    subcatList = CategoryItem.query.filter_by(subCat=subcat).all()
    subcatItemList = []
    for category in subcatList:
        item = Carousel.query.filter_by(subCat=category).all()
        if (len(itemList)):
            subcatItemList.append(item)
    if (len(itemList)):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "items": [carouselItem.json() for carouselItem in itemList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no items donated under this Sub-category"
        }
    ), 404

# WISHLIST
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

if __name__ == "__main__":
    app.run(port="5003", debug=True)
