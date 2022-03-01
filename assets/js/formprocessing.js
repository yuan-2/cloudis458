// Posting data to backend
function submitForm(formName) {
    var formElements = document.forms[0].elements

    var formData = new FormData();
    formData.append("formName", formName);

    for (ele in formElements) {
        var eleId = formElements[ele].id;
        var eleType = formElements[ele].type;
        // console.log("Name: " + formElements[ele].name + ", Type: " + formElements[ele].type)
        if (eleType == "radio") {
            var eleName = formElements[ele].name;
            if (!formData.has(eleName)) {
                formData.append(eleName, document.querySelector(`input[name='${eleName}']:checked`).value);
                // console.log(document.querySelector("input[name='"+eleName+"']:checked").value)
            }
        }
        else if (eleType == "checkbox") {
            // store all values as a single string, values separated by ;
            var eleName = formElements[ele].name;
            if (!formData.has(eleName)) {
                checkedBoxes = document.querySelectorAll(`input[name='${eleName}']:checked`);
                values = "";
                for ( let box of checkedBoxes) {
                    values += box.value + ";"
                }
                formData.append(eleName, values.slice(0,-1));
            }
        }
        else if (eleType == "file") {
            formData.append(eleId, formElements[ele].files[0].name);
            formData.append("file" + eleId, formElements[ele].files[0]);
        }
        else {
            formData.append(eleId, formElements[ele].value);
        }
    }

    addDonation(formData, 'http://ec2-13-229-105-254.ap-southeast-1.compute.amazonaws.com:5003/formanswers')
    alert("Item has been posted successfully")
    // error msg pls add
    window.location = window.location;
}

// POST request:
async function addDonation(data, url) {
    // Default options are marked with *
    // console.log(data)

    const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'no-cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: data // body data type must match "Content-Type" header
    });
    
    console.log(response.message)

    return "OK"; // parses JSON response into native JavaScript objects
}