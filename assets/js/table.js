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
                // for (var i in result.data) {
                    // console.log(Object.keys(result.data))
                    // console.log(i.toString());
                    // attributes = Object.keys(result.data);
                    // id = attributes[i];
                    // console.log(id);
                //     if (i != "fileName") {
                //         console.log(i, result.data.i)
                //         document.getElementById(i).value = result.data[i];
                //     }
                // }
                // console.log(document.getElementById('itemName'));
                document.getElementById("itemName").value = result.data.itemName;
                document.getElementById("description").value = result.data.description;
                document.getElementById("donorName").value = result.data.donorName;
                document.getElementById("donorAddr").value = result.data.donorAddr;
                document.getElementById("contactNo").value = result.data.contactNo;
                document.getElementById("category").value = result.data.category;
                document.getElementById("quantity").value = result.data.quantity;
                document.getElementById("needDelivery").value = result.data.requireDelivery;
                document.getElementById("region").value = result.data.region;
                document.getElementById("itemStatus").value = result.data.itemStatus;
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
    data["id"] = document.getElementById("itemID").value;
    data["itemName"] = document.getElementById("itemName").value;
    data["description"] = document.getElementById("description").value;
    data["donorName"] = document.getElementById("donorName").value;
    data["donorAddr"] = document.getElementById("donorAddr").value;
    data["contactNo"] = document.getElementById("contactNo").value;
    data["itemCategory"] = document.getElementById("itemCat").value;
    data["quantity"] = document.getElementById("quantity").value;
    data["requireDelivery"] = document.getElementById("needDelivery").value;
    data["region"] = document.getElementById("area").value;
    data["itemStatus"] = document.getElementById("status").value;
    // data["fileName"] = document.getElementById("file").value;
    var jsondata = JSON.stringify(data);
    $(async () => {
        var serviceURL = "http://127.0.0.1:5000/updateItem/" + data.id;
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
                document.getElementById("itemName").value = result.data.itemName;
                document.getElementById("remarks").value = result.data.remarks;
                document.getElementById("itemCat").value = result.data.category;
                document.getElementById("status").value = result.data.itemStatus;
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
    data["id"] = document.getElementById("id").value;
    data["itemName"] = document.getElementById("itemName").value;
    data["remarks"] = document.getElementById("remarks").value;
    data["itemCategory"] = document.getElementById("itemCat").value;
    data["itemStatus"] = document.getElementById("status").value;
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
                document.getElementById("reqID").value = result.data.reqid;
                document.getElementById("requestorName").value = result.data.requestor;
                document.getElementById("deliveryLocation").value = result.data.deliveryLocation;
                document.getElementById("itemCat").value = result.data.itemCategory;
                document.getElementById("quantity").value = result.data.requestQty;
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
    data["reqid"] = document.getElementById("reqID").value;
    data["requestor"] = document.getElementById("requestorName").value;
    data["deliveryLocation"] = document.getElementById("deliveryLocation").value;
    data["itemCategory"] = document.getElementById("itemCat").value;
    data["requestQty"] = document.getElementById("quantity").value;
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

