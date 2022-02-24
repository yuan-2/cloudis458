// get column headers

$(document).ready(function() {
    $('#example').DataTable( {
        ajax: {
            url: 'sth',
            dataSrc: 'data',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            type: "GET",
            dataType: "json"
        },
        columns: [ 
            { data: 'sth' }
        ],
        fixedHeader: true,
    });

} );    

function editSpecificRow(form) {
    document.getElementById("edit-section").innerHTML += "<br>" + 
                                                            "<button type='button' id='save-btn' class='btn btn-outline-secondary' onclick='edit" + form + "()'>Save Changes</button>" 
    document.getElementById("edit-section").style.display = "block";
    if (form == "Inventory" || form == "Wishlist") {
        document.querySelector('[placeholder="submissionID"]').setAttribute("onchange", "fill" + form + "Details(this.value)");
        if (form == "Inventory") {
            document.getElementById("edit-photo").style.display = "none";
        }
    }
    else if (form == "SuccessfulMatches") {
        document.getElementById('0').setAttribute("onchange", "fill" + form + "Details(this.value)");
    }
}

function getEditDetails(fields) {
    columnDetails = fields["columnDetails"];
    fieldArr = []
    for (field in fields) {
        fieldObj = {}
        for (fieldID in columnDetails) {
            if (columnDetails[fieldID] == field) {
                fieldObj["fieldID"] = fieldID;
                fieldObj["fieldName"] = field;
                fieldObj["fieldType"] = typeof(fields[field])
                fieldObj["placeholder"] = field;
                fieldObj["formName"] = "edit-section";
            }
        }
        if (field == "submissionID" || field == "matchID") {
            fieldArr.unshift(fieldObj);
        }
        else if (field != "timeSubmitted") {
            if (field != "matchDate") {
                fieldArr.push(fieldObj);
            }
        }
    }
    for (i = 0; i < fieldArr.length - 1; i++) {
        fieldInput = fieldArr[i];
        if (fieldInput.fieldType == "string") {
            buildText(fieldInput);
        }
        else if (fieldInput.fieldType == "number") {
            buildNumber(fieldInput);
        }
    }
}

function fillRequestDetails(val) {
    $(async () => {
        var serviceURL = "http://127.0.0.1:5000/getRequests/" + val;
        try {
            const response =
            await fetch(
                serviceURL, { 
                method: 'GET',
                headers: { 'Content-Type': 'application/json'},
            });
            const result = await response.json();
            if (response.status == 200) {
                // success case
                for (var i in result.data) {
                    if (i != "timeSubmitted" && i != "requestorContactNo") {
                        document.getElementById(i).value = result.data[i];
                    }
                }

            }
            if (response.status == 404) {
                alert('There is no such request ID in the database, please enter a valid ID.')
            }
        }
        catch (error) {
            // Errors when calling the service; such as network error, 
            // service offline, etc
            alert('There is a problem retrieving the data, please try again later.');
        } // error
    });
}

function editRequest() {
    var data = {};
    var inputFields = document.getElementById("edit-section").children;
    for (var i in inputFields) {
        input = inputFields[i];
        inputChildrenCount = input.childElementCount;
        inputChildren = inputFields[i].children;
        if (inputChildrenCount > 0) {
            for (j = 0; j < inputChildrenCount; j++) {
                inputChildElement = inputChildren[j].children[1];
                data[inputChildElement.id] = inputChildElement.value;
            }
        }
    }
    var jsondata = JSON.stringify(data);
    $(async () => {
        var serviceURL = "http://127.0.0.1:5000/updateRequest/" + data.reqid;
        try {
            const response =
            await fetch(
                serviceURL, { 
                method: 'PUT',
                headers: { 'Content-Type': 'application/json'},
                body: jsondata,
            });
            const result = await response.json();
            if (response.status == 200) {
                // success case
                alert('Successfully updated data in database. Please refresh to view changes.')
                window.location.reload();
            }
            }
        catch (error) {
            // Errors when calling the service; such as network error, 
            // service offline, etc
            alert('There is a problem updating the data, please try again later.');
        } // error
    });
}

function fillSuccessfulMatchesDetails(val) {
    $(async () => {
        var serviceURL = "http://127.0.0.1:5000/getSuccessfulMatches/" + val;
        try {
            const response =
            await fetch(
                serviceURL, { 
                method: 'GET',
                headers: { 'Content-Type': 'application/json'},
            });
            const result = await response.json();
            if (response.status == 200) {
                // success case
                for (var i in result.data) {
                    console.log(i, result.data[i]);
                    for (id in result.columnHeaders) {
                        // console.log(id, result.columnHeaders[id]);
                        if (result.columnHeaders[id] == i) {
                            document.getElementById(id).value = result.data[i];
                        }
                    }
                }
            }
            if (response.status == 404) {
                alert('There is no such request ID in the database, please enter a valid ID.')
            }
        }
        catch (error) {
            // Errors when calling the service; such as network error, 
            // service offline, etc
            alert('There is a problem retrieving the data, please try again later.');
        } // error
    });
}

function editSuccessfulMatches() {
    var data = {};
    var inputFields = document.getElementById("edit-section").children;
    var matchID = document.getElementById("0").value;
    for (var i in inputFields) {
        input = inputFields[i];
        inputChildrenCount = input.childElementCount;
        inputChildren = inputFields[i].children;
        if (inputChildrenCount > 0) {
            inputChildElement = inputChildren[1];
            inputLabelElement = inputChildren[0];
            data[inputChildElement.id] = inputChildElement.value;
            data[inputLabelElement.innerHTML] = inputChildElement.value;
        }
}
    var jsondata = JSON.stringify(data);
    $(async () => {
        var serviceURL = "http://127.0.0.1:5000/updateSuccessfulMatches/" + matchID;
        try {
            const response =
            await fetch(
                serviceURL, { 
                method: 'PUT',
                headers: { 'Content-Type': 'application/json'},
                body: jsondata,
            });
            const result = await response.json();
            if (response.status == 200) {
                // success case
                alert('Successfully updated data in database. Please refresh to view changes.')
                window.location.reload();
            }
            }
        catch (error) {
            // Errors when calling the service; such as network error, 
            // service offline, etc
            alert('There is a problem updating the data, please try again later.');
        } // error
    });
}

