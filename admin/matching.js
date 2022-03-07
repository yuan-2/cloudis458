// 1. get list of migrant workers who wants the item (from request table) & have the highest priority
// first criteria is the no. of times migrant worker gotten an item before
function getAllMWReqForItem(itemID) {
    $(async () => {
        var serviceURL = "http://127.0.0.1:5000/getRankByReqHistory/" + itemID;
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
                // document.getElementById("quantity").value = result.data.requestQty;
                listofMW = result.data;
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

// 2. afterwards, check each MW whether if anyone opted for self pick-up & prioritise them first
// else, continue with the current list of MWs

// 3. check for the list of MWs, how long since each of them have gotten an item

// 4. check how far is MW away from delivery driver


// 2. for each migrant worker, check their eligibility (get their no.)


// 3. find the highest prioritised migrant worker and match the mw to the item/donor

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