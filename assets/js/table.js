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
    if (form == "Inventory") {
        document.querySelector('[placeholder="donationID"]').setAttribute("onchange", "fillCarouselDetails(this.value)");
        document.getElementById("edit-photo").style.display = "none";
    }
    else if (form == "Wishlist") {
        document.querySelector('[placeholder="wishlistID"]').setAttribute("onchange", "fillWishlistDetails(this.value)");
    }
    else if (form == "Request") {
        document.querySelector('[placeholder="reqID"]').setAttribute("onchange", "fillRequestDetails(this.value)");
    }
    else if (form == "SuccessfulMatches") {
        document.querySelector('[placeholder="matchID"]').setAttribute("onchange", "fillSuccessfulMatchesDetails(this.value)");
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
        if (field == "reqID") {
            fieldArr.unshift(fieldObj);
        }
        else if (["donationID", "wishlistID", "matchID"].includes(field)) {
            fieldArr.unshift(fieldObj);
        }
        else if (field != "timeSubmitted") {
            if (field != "matchDate" && field != "Item Photo" && field != "itemName") {
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



