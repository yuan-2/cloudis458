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
              <label for="` + field.fieldName +`" class="form-label">` + field.fieldName + `</label>
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
              <label for="` + field.fieldName +`" class="form-label">` + field.fieldName + `</label>
              <select class="form-select" name="` + field.fieldName +`">`;
    
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
              <label for="` + field.fieldName +`" class="form-label">` + field.fieldName + `</label>
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