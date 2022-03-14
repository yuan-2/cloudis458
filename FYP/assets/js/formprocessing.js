function submitForm(formName) {
    var donateFormElements = document.forms[0].elements

    // console.log(donateFormElements);

    var formData = new FormData();
    formData.append("formName", formName);

    for (ele in donateFormElements) {
        var eleId = donateFormElements[ele].id;
        var eleType = donateFormElements[ele].type;
        // console.log("Name: " + donateFormElements[ele].name + ", Type: " + donateFormElements[ele].type)
        if (eleType == "radio") {
            var eleName = donateFormElements[ele].name;
            formData.append(eleName, document.querySelector(`input[name='${eleName}']:checked`).value)
            // console.log(document.querySelector("input[name='"+eleName+"']:checked").value)
        }
        else if (eleType == "file") {
            formData.append(eleId, donateFormElements[ele].files[0].name)
            formData.append("file" + eleId, donateFormElements[ele].files[0])
        }
        else {
            formData.append(eleId, donateFormElements[ele].value)
        }
    }


    addDonation(formData, 'http://127.0.0.1:5005/formanswers')
    alert("Item has been posted successfully")
}

// Example POST method implementation:
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