// get requests for specific item, then get each eligibility of migrant worker, then compare their eligibilities

function matchItem(item) {
    $(async () => {
        var serviceURL = "http://127.0.0.1:5000/getRequests/" + item;
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
    })
    
}


function updateEligibility(migrantContactNo) {
    var data = {};
    data["reqid"] = document.getElementById("reqID").value;
    data["requestor"] = document.getElementById("requestorName").value;
    data["deliveryLocation"] = document.getElementById("deliveryLocation").value;
    data["itemCategory"] = document.getElementById("itemCat").value;
    data["requestQty"] = document.getElementById("quantity").value;
    var jsondata = JSON.stringify(data);
    console.log(jsondata);

    $(async () => {
        var serviceURL = "http://127.0.0.1:5004/updateEligibility/" + migrantContactNo;
        try {
            const response =
            await fetch(
                serviceURL, { 
                method: 'PUT',
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
    })
}