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

function editSpecificRow() {
    document.getElementById("edit-section").style.display = "block";
    document.getElementById("edit-photo").style.display = "none";
}

function fillInventoryDetails(val) {
    $(async () => {
        var serviceURL = "http://127.0.0.1:5000/getItem/" + val;
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
                    if (i != "fileName" && i != "id" && i != "timeSubmitted") {
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

function editInventory() {
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
        var serviceURL = "http://127.0.0.1:5000/updateItem/" + data.itemID;
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

function editPhoto() {
    document.getElementById("edit-section").style.display = "none";
    document.getElementById("edit-photo").style.display = "block";
}

function editPhotoFile() {
    var data = {};
    var editElements = document.getElementById("edit-photo").children;
    for (child in editElements) {
        // console.log(editElements[child].children);
        childElement = editElements[child].children;
        if (childElement != undefined) {
            for (innerChild in childElement) {
                if (childElement[innerChild].type == 'number') {
                    data['id'] = childElement[innerChild].value;
                }
                else if (childElement[innerChild].type == 'file') {
                    data[childElement[innerChild].name] = childElement[innerChild].files[0].name;
                    data['file'] = childElement[innerChild].files[0];
                }
            }
        }
    }
    var jsondata = JSON.stringify(data);
    $(async () => {
        var serviceURL = "http://127.0.0.1:5000/updatePhoto/" + data.id;
        try {
            const response =
            await fetch(
                serviceURL, { 
                method: 'POST',
                mode: 'no-cors', // no-cors, *cors, same-origin
                cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
                credentials: 'same-origin', // include, *same-origin, omit
                redirect: 'follow', // manual, *follow, error
                referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
                body: jsondata,
            });
            const result = await response.json();
            if (response.status == 200) {
                // success case
                alert('Successfully updated photo in database. Please refresh to view changes.')
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

function fillWishlistDetails(val) {
    $(async () => {
        var serviceURL = "http://127.0.0.1:5000/getWishlist/" + val;
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
                    if (i != "timeSubmitted") {
                        document.getElementById(i).value = result.data[i];
                        console.log(document.getElementById(i).value, result.data[i]);
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

function editWishlist() {
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
        var serviceURL = "http://127.0.0.1:5000/updateWishlist/" + data.id;
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

function fillMatchDetails(val) {
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
                    if (i != "dateSubmitted" && i != "matchid") {
                        document.getElementById(i).value = result.data[i];
                        // console.log(document.getElementById(i).value, result.data[i]);
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
    console.log(data);
    var jsondata = JSON.stringify(data);
    $(async () => {
        var serviceURL = "http://127.0.0.1:5000/updateSuccessfulMatches/" + data.reqid;
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

