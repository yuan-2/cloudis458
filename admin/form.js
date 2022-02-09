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
            
            // if admin page --> change as needed or check if admin is logged in
            if (window.location.href.indexOf("admin") > -1) {
                addIcons();
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
                            <label for="` + field.fieldName + `" class="form-label">` + field.fieldName + `</label>
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

    var optionNo = 1;
    for (var option of options) {
        checkboxField +=
            `<input id="` + optionNo + `" class="form-check-input" type="checkbox" name="` + field.fieldName + `" value="` + option + `">
                    <label for="` + optionNo + `" class="form-check-inline" style="padding-right: 7px;" >` + option + `</label>`;
        optionNo++;
    }

    checkboxField += `</div>`;

    document.getElementById(field.formName).innerHTML += checkboxField;
}

// add edit icons to each field
function addIcons() {
    var editIcon = ` <i type="button" class="bi bi-pencil m-1" style="font-size:14px"></i>`;
    $('label.form-label').each(function() {
        $(this).after(editIcon);
    });
};
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

// DISPLAYING EDITING FORM
//#region 
function showFieldType(){
    var inputType = $("#fieldType :selected").val();
    if (inputType == "text") {
        if ($('#textInput').length == 0) {
            $('#newField').append(`<div id="textInput">
                                    <input type="text" class="form-control" id="placeholder" placeholder="Enter placeholder text here (optional)">
                                </div>`);
        }
        $('#addOptions').hide();
        $('#textInput').show();
    } else if (inputType == "radio" || inputType == "dropdown" || inputType == "checkbox"){
        if ($('#addOptions').length == 0) {
            $('#newField').append(`<div id="addOptions"><ol id="optionsList"></ol></div>`)
            addOption();
            $('#addOptions').append(`<button class="btn btn-outline-secondary ms-3" type='button' id="addOptionBtn"
                                    onclick="addOption()">+ Add Option</button>`);
        }
        $('#textInput').hide();
        $('#addOptions').show();
    } else {
        $('#textInput').hide();
        $('#addOptions').hide();
    }
}

function addOption(){
    var option = `<li><div class="input-group">
                        <input type="text" class="form-control mb-3" name="option" placeholder="Enter new option">
                        <button type="button" onclick="removeOption(this)" class="btn-close m-2" aria-label="Close"></button>
                    </div></li>`;
    $('#optionsList').append(option);
}

function removeOption(elem){
    elem.parentNode.parentNode.remove();
}
//#endregion

// FORM CRUD
//#region 
async function addField(formName) {
    var fieldName = $('#fieldName').val();
    var fieldType = $('#fieldType').val();
    if (fieldType == "text") {
        var placeholder = $('#placeholder').val();
        var fieldData = JSON.stringify({formName: formName, fieldName: fieldName, fieldType: fieldType, placeholder: placeholder})
    } else if (fieldType == "radio" || fieldType == "dropdown" || fieldType == "checkbox"){
        var options = '';
        $("[name='option']").each(function() {
            options += this.value + ';';
        });
        options = options.slice(0,-1);
        var fieldData = JSON.stringify({formName: formName, fieldName: fieldName, fieldType: fieldType, options: options})
    } else {
        var fieldData = JSON.stringify({formName: formName, fieldName: fieldName, fieldType: fieldType})}

    var serviceURL = "http://127.0.0.1:5003/formbuilder";

    return fetch (serviceURL,
    {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: fieldData
    })
    .then(response => response.json())
    .then(data => {
        // console.log(data);
        window.location = window.location;
    })
};
//#endregion