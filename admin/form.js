// FORM BUILDING
//#region 
async function retrieveForm(formName) {
    var serviceURL = "http://127.0.0.1:5003/formbuilder/" + formName;

    try {
        // Retrieve list of all fields
        const response =
            await fetch(
                serviceURL, { method: 'GET' }
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
        }
    } catch (error) {
        // Errors when calling the service; such as network error, 
        // service offline, etc
        console.log(error)
        alert('There is a problem retrieving data, please refresh the page or try again later.');
    } // error
}

function buildRadio(field) {

    var radioField = `
            <div class="col-6">
              <label for="` + field.fieldName + `" class="form-label">` + field.fieldName + `</label>
              <br>`;

    var options = field.options.split(";");

    for (var option of options) {
        radioField +=
            `<label class="radio-inline" style="padding-right: 7px;" >
                        <input class="form-check-input" type="radio" name="` + field.fieldName + `" value="` + option + `"> ` + option + `
                    </label>`;
    }

    radioField += `</div>`;

    document.getElementById(field.formName).innerHTML += radioField;
}

function buildText(field) {
    var textField = `<div class="col-md-6">
                        <label for="` + field.fieldName + `" class="form-label">` + field.fieldName + `</label>
                        <input type="text" class="form-control" id="` + field.fieldName + `" placeholder="` + field.placeholder + `">
                    </div>`;


    document.getElementById(field.formName).innerHTML += textField;
}

function buildNumber(field) {
    var numField = `<div class="col-md-6">
                        <label for="` + field.fieldName + `" class="form-label">` + field.fieldName + `</label>
                        <input type="number" class="form-control" id="` + field.fieldName + `">
                    </div>`;


    document.getElementById(field.formName).innerHTML += numField;
}

function buildFile(field) {
    var fileField = `<div class="col-6">
                        <div class="form-group">
                            <label for="` + field.fieldName + `">` + field.fieldName + `</label>
                            <br>
                            <input type="file" class="form-control-file" id="` + field.fieldName + `" style='padding-top: 10px;'>
                        </div>
                    </div>`;

    document.getElementById(field.formName).innerHTML += fileField;
}

function buildDropdown(field) {
    var dropdownField = `
            <div class="col-6">
              <label for="` + field.fieldName + `" class="form-label">` + field.fieldName + `</label>
              <select class="form-select" name="` + field.fieldName + `">`;

    if (field.options != null) {
        var options = field.options.split(";");
        for (var option of options) {
            dropdownField += `<option value="` + option + `"> ` + option + `</option>`;
        }
    }

    dropdownField += `</select></div>`;

    document.getElementById(field.formName).innerHTML += dropdownField;
}

function buildCheckbox(field) {

    var checkboxField = `
            <div class="col-6">
              <label for="` + field.fieldName + `" class="form-label">` + field.fieldName + `</label>
              <br>`;

    var options = field.options.split(";");

    for (var option of options) {
        radioField +=
            `<input class="form-check-input" type="checkbox" name="` + field.fieldName + `" value="` + option + `">
                    <label class="form-check-inline" style="padding-right: 7px;" >` + option + `</label>`;
    }

    checkboxField += `</div>`;

    document.getElementById(field.formName).innerHTML += checkboxField;
}
//#endregion

// POPULATING ITEM CATEGORIES AND NAMES DROPDOWN LISTS
//#region 
function checkLogin() {

    getDropDownCat().then(function autoPopCategories(result) {
        var catList = result
        // reset dropdown fields
        $('#itemCategoryOptions').html("");
        // Start off with an empty selected option for category
        $('#itemCategoryOptions').append(`<option selected> </option>`);

        for (cat of catList) {
            $('#itemCategoryOptions').append(`
                <option value="${cat}">${cat}</option>
            `);
        }
    }
    )
    if (window.sessionStorage.getItem("userType") != null) {
        userType = window.sessionStorage.getItem("userType")
        document.getElementById("loginLogoutButton").innerText = "Logout"
    }
}

async function getDropDownCat() {
    let response = await fetch("http://127.0.0.1:5004/getCat")
    let responseCode = await response.json()

    if (responseCode.code == 200) {
        return responseCode.data.categories
    } else {
        alert(responseCode.message)
    }
}

async function populateItemNames(cat) {
    $('#itemNameOptions').html("");
    cat = cat.value
    let response = await fetch("http://127.0.0.1:5004/getItemsInCat/" + cat)
    let responseCode = await response.json()

    if (responseCode.code == 200) {
        $('#itemNameOptions').append("<option selected> </option>");
        for (cat of responseCode.data.itemsInCat) {
            $('#itemNameOptions').append(`<option>${cat.itemName}</option>`)
        }
    }
}
//#endregion

// EDITING FORM
//#region 
function showInputType(){
    var inputType = $("#inputType :selected").val();
    if (inputType == "text") {
        if ($('#textInput').length == 0) {
            $('#newInput').append(`<div id="textInput">
                                    <input type="text" class="form-control" id="placeholder" placeholder="Enter placeholder text here (optional)">
                                </div>`);
        }
        $('#addOptions').hide();
        $('#textInput').show();
    } else if (inputType == "radio" || inputType == "dropdown" || inputType == "checkbox"){
        if ($('#addOptions').length == 0) {
            $('#newInput').append(`<div id="addOptions"><ol id="optionsList"></ol></div>`)
            addOptionField();
            $('#addOptions').append(`<button class="btn btn-outline-secondary ms-3" type='button' id="add-input"
                                    onclick="addOptionField()">+ Add Option</button>`);
        }
        $('#textInput').hide();
        $('#addOptions').show();
    } else {
        $('#textInput').hide();
        $('#addOptions').hide();
    }
}

function addOptionField(){
    var optionField = `<li><div class="input-group">
                        <input type="text" class="form-control mb-3" name="option" placeholder="Enter new option">
                        <button type="button" onclick="removeOption(this)" class="btn-close m-2" aria-label="Close"></button>
                    </div></li>`;
    $('#optionsList').append(optionField);
}

function removeOption(elem){
    elem.parentNode.parentNode.remove();
}
//#endregion