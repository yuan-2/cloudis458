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
    document.getElementById("carousel").style.display = "none";
    if (form == "Inventory") {
        document.querySelector('[placeholder="carouselID"]').setAttribute("onchange", "fillCarouselDetails(this.value)");
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
        else if (["carouselID", "wishlistID", "matchID"].includes(field)) {
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

async function getDropDownCat() {
    let response = await fetch("http://127.0.0.1:5003/getCat")
    let responseCode = await response.json()

    if (responseCode.code == 200) {
        return responseCode.data.categories
    } else {
        alert(responseCode.message)
    }
}

async function retrieveFormAdmin(formName) {
    document.getElementById("edit-section").style.display = "none";
    document.getElementById("edit-photo").style.display = "none";
    document.getElementById("carousel").style.display = "block";
    var serviceURL = "http://127.0.0.1:5003/formbuilder/" + formName;

    try {
        // Retrieve list of all fields
        const response =
            await fetch(
                serviceURL, {
                    method: 'GET'
                }
            );
        const result = await response.json();
        if (response.ok) {
            // success case
            var allFields = result.data.items;
            for (field of allFields) {
                if (field.fieldType == "radio") {
                    buildRadio(field);
                }
                if (field.fieldType == "text") {
                    buildText(field);
                }
                if (field.fieldType == "checkbox") {
                    buildCheckbox(field);
                }
                if (field.fieldType == "file") {
                    buildFile(field);
                }
                if (field.fieldType == "dropdown") {
                    buildDropdown(field);
                }
                if (field.fieldType == "number") {
                    buildNumber(field);
                }
            }

            // if edit page --> change as needed
            if ($('body').is('.editForm')) {
                addIcons(formName);
            }

            var contactField = `<div id="contactField" class="col-md-6">
                                    <label for="contactNo" class="form-label">Contact Number</label>
                                    <input required type="number" class="form-control" id="contactNo">
                                </div>`
            var itemNameField = `<!--On change of this dropdown, auto get item names listed under this category-->
                                <div class="col-6">
                                    <label for="itemCategoryOptions" class="form-label">Item Category</label>
                                    <select onchange="populateSubCat(this)" class="form-select" id="itemCategoryOptions" name="category"
                                        required>
                                        <!--Dynamically dropdown categories listed in existing db-->
                                    </select>
                                </div>`
            var subCatField = `<div class="col-6">
                                    <label for="subCatOptions" class="form-label">Sub-Category</label>
                                    <select onchange="populateItemNames(this)" class="form-select" id="subCatOptions" name="subcat"
                                        required>
                                        <!--Dynamically dropdown subcats listed in existing db-->
                                    </select>
                                </div>`
            var catField = `<!--Option value for item name needs to be dynamic, based on category-->
                                <div class="col-6">
                                    <label for="itemNameOptions" class="form-label">Item Name</label>
                                    <select class="form-select" id="itemNameOptions" name="itemName" required>
                                        <!--Dynamically update item names-->
                                    </select>
                                </div>`;
            var addButton = `<br><button type="button" onclick="submitForm('carousel')" class="btn btn-outline-secondary col-2">Submit</button>`

            // document.getElementById('contactField').innerHTML += contactField;
            document.getElementById(formName).innerHTML += contactField + itemNameField + subCatField + catField + addButton;

            getDropDownCat().then(function autoPopCategories(result) {
                var catList = result
        
                // reset dropdown fields
                $('#itemCategoryOptions').html("")
                $('#itemNameOptions').html("")
                $('#subCatOptions').html("")
        
                // Start off with an empty selected option for category
                $('#itemCategoryOptions').append(`<option disabled selected> </option>`)
                $('#subCatOptions').append("<option disabled selected> Please select a category first </option>")
                $('#itemNameOptions').append("<option disabled selected> Please select a sub-category first </option>")
        
                for (cat of catList) {
                    $('#itemCategoryOptions').append(`
                        <option value="${cat}">${cat}</option>
                    `)
                }
            })
                
        }
    } catch (error) {
        // Errors when calling the service; such as network error, 
        // service offline, etc
        console.log(error)
        alert('There is a problem retrieving data, please refresh the page or try again later.');
    } // error
}

function deleteRow() {
    document.getElementById("edit-section").innerHTML = `<div class='col-md-6'>
                                                            <label for="carouselID" class="form-label">carouselID</label>
                                                            <input required type="text" class="form-control" id="carouselID" placeholder="carouselID"> 
                                                            <br>
                                                            <button type='button' id='save-btn' class='btn btn-outline-secondary' onclick='confirmDeleteRow()'>Delete Row</button>
                                                        </div>`;
    document.getElementById("edit-section").style.display = "block";
    document.getElementById("carousel").style.display = "none";
}

function confirmDeleteRow() {
    $(async () => {
        val = document.getElementById("carouselID").value
        var serviceURL = "http://127.0.0.1:5003/deleteRow/" + val;
        try {
            const response =
            await fetch(
                serviceURL, { 
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json'},
            });
            const result = await response.json();
            if (response.status == 200) {
                // success case
                alert("The data has been deleted successfully.")
                window.location.reload();
            }
            if (response.status == 404) {
                alert('There is no such row in the database, please enter a valid ID.')
            }
        }
        catch (error) {
            // Errors when calling the service; such as network error, 
            // service offline, etc
            alert('There is a problem deleting the data, please try again later.');
        } // error
    });

}

