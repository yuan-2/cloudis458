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

class NewCarousel(db.Model):
    __tablename__ = 'newcarousel'
    
    carouselID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donorID = db.Column(db.Integer)
    submissionID = db.Column(db.String(30), nullable=False)
    itemName = db.Column(db.String(50), nullable=False)
    itemCategory = db.Column(db.String(50), nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)
    itemStatus = db.Column(db.String(50), nullable=False)
        
    def json(self):
        return {"carouselID": self.carouselID, "donorID": self.donorID, "submissionID": self.submissionID, "itemName": self.itemName, "itemCategory": self.itemCategory, "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus}

class NewWishlist(db.Model):
    __tablename__ = 'newwishlist'
    
    wishlistID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    migrantID = db.Column(db.Integer)
    submissionID = db.Column(db.String(30), nullable=False)
    itemName = db.Column(db.String(50), nullable=False)
    itemCategory = db.Column(db.String(50), nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)
    itemStatus = db.Column(db.String(50), nullable=False)
        
    def json(self):
        return {"wishlistID": self.wishlistID, "migrantID": self.migrantID, "submissionID": self.submissionID, "itemName": self.itemName, "itemCategory": self.itemCategory, "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus}



# FORMBUILDER
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


# FORMANSWERS + CAROUSEL/WISHLIST
# get all answers by submission
@app.route("/formanswers/<string:submissionID>")
def getAllAnswersBySubmission(submissionID):
    answerlist = FormAnswers.query.filter_by(submissionID=submissionID).all()
    if len(answerlist):

        # map answers to field names
        mappedAnswerlist = {}
        for answer in answerlist:
            field = FormBuilder.query.filter_by(fieldID=answer.fieldID).options(load_only('fieldName')).first()
            mappedAnswerlist[field.fieldName] = answer.answer

        # check if submission from carousel or wishlist
        submission = NewCarousel.query.filter_by(submissionID=submissionID).first()
        if submission is None:
            submission = NewWishlist.query.filter_by(submissionID=submissionID).first()

        if submission is not None:
            return jsonify(
                {
                    "code": 200,
                    "data": dict(submission.json(), **mappedAnswerlist)
                }
            )
    return jsonify(
        {
            "code": 404,
            "message": "There are no answers for the submission."
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
        submission = NewWishlist(**details)
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
        submission = NewCarousel(**details)
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

if __name__ == "__main__":
    app.run(port="5003", debug=True)
