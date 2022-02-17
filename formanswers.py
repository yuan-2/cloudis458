from ast import For
from fileinput import filename
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
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

class FormAnswers(db.Model):
    __tablename__ = 'formanswers'

    answerID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    submissionID = db.Column(db.String(30), nullable=False)
    # , db.ForeignKey(Learner.empID)
    migrantID = db.Column(db.Integer)
    donorID = db.Column(db.Integer)
    formName = db.Column(db.String(15), nullable=False)
    fieldID = db.Column(db.Integer, nullable=False)
    answer = db.Column(db.String(50), nullable=False)

    def json(self):
        return {"answerID": self.answerID, "submissionID": self.submissionID, "migrantID": self.migrantID, "donorID": self.donorID, "fieldID": self.fieldID, "formName": self.formName, "answer": self.answer}

# get all fields by form
@app.route("/formanswers/<int:submissionID>")
def getAllAnswersBySubmission(submissionID):
    answerlist = FormAnswers.query.filter_by(submissionID=submissionID).all()
    if len(answerlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "items": [answer.json() for answer in answerlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no answer for the submission."
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

    submission = {}
    for id in formDict:
        answer = {"submissionID": submissionID, "formName": formName, "fieldID": id, "answer": formDict[id]}
        if formName == "donate":
            answer['donorID'] = userid
        elif formName == "request":
            answer['migrantID'] = userid
        item = FormAnswers(**answer)
        item.submissionID = submissionID
        if ( id.isdigit() ): 
            try:
                db.session.add(item)
                db.session.commit()
                submission[item.fieldID] = item.json()
            except Exception as e:
                print(e)
                return jsonify({
                    "message": "Unable to commit to database.",
                    "data" : item.json()
                }), 500
    
    return jsonify(submission), 201



if __name__ == "__main__":
    app.run(port="5005", debug=True)
