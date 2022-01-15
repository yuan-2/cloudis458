$(document).ready(function() {
    $('#inventory').DataTable( {
        ajax: {
            url: 'http://127.0.0.1:5000/getAllItems',
            dataSrc: 'data.items',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            type: "GET",
            dataType: "json"
        },
        columns: [
            { data: 'id' },
            { data: 'name' },
            { data: 'description' },
            { data: 'donorName' },
            { data: 'donorAddr' },
            { data: 'contactNo' },
            { data: 'category' },
            { data: 'quantity' },
            { data: 'requireDelivery' },
            { data: 'region' },
            { data: 'timeSubmitted' }, 
            { data: 'itemStatus' }
        ],
        // responsive: true,
        fixedHeader: true,
        // "scrollX": true,
        // scrollY: 200,
        // deferRender: true,
        // scroller: true, 
    });

    $('#requests').DataTable( {
        ajax: {
            url: 'http://127.0.0.1:5000/getRequests',
            dataSrc: 'data',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            type: "GET",
            dataType: "json"
        },
        columns: [
            { data: 'reqid' },
            { data: 'requestor' },
            { data: 'deliveryLocation' },
            { data: 'itemCategory' },
            { data: 'requestQty' },
            { data: 'timeSubmitted' }
        ],
        fixedHeader: true,
    });

    $('#wishlist').DataTable( {
        ajax: {
            url: 'http://127.0.0.1:5000/getWishlist',
            dataSrc: 'data',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            type: "GET",
            dataType: "json"
        },
        columns: [
            { data: 'id' },
            { data: 'itemName' },
            { data: 'remarks' },
            { data: 'category' },
            { data: 'timeSubmitted' },
            { data: 'itemStatus' }
        ],
        fixedHeader: true,
    });

    $('#successMatches').DataTable( {
        ajax: {
            url: 'http://127.0.0.1:5000/getSuccessfulMatches',
            dataSrc: 'data',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            type: "GET",
            dataType: "json"
        },
        columns: [
            { data: 'matchid' },
            { data: 'reqid' },
            { data: 'requestorName' },
            { data: 'requestorContactNo' },
            { data: 'donorName' },
            { data: 'donorContactNo' },
            { data: 'requestedItem' },
            { data: 'itemCategory' },
            { data: 'dateSubmitted' }
        ],
        fixedHeader: true,
        responsive: true,
    });

    $('#example').DataTable( {
        fixedHeader: true,
    });

} );    

function editSpecificRow() {
    document.getElementById("edit-section").style.display = "block";
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
                document.getElementById("itemName").value = result.data.name;
                document.getElementById("description").value = result.data.description;
                document.getElementById("donorName").value = result.data.donorName;
                document.getElementById("donorAddr").value = result.data.donorAddr;
                document.getElementById("contactNo").value = result.data.contactNo;
                document.getElementById("itemCat").value = result.data.category;
                document.getElementById("quantity").value = result.data.quantity;
                document.getElementById("needDelivery").value = result.data.requireDelivery;
                document.getElementById("area").value = result.data.region;
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
    console.log(jsondata);
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

