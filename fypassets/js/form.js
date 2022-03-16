user = ""

// FORM BUILDING
//#region 
async function retrieveForm(formName) {

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

            // compulsory fields
            var disable = ""
            if (formName == "wishlist") {
                disable = "disabled"
            }
            // console.log(user.username)
            var contactField = `<label for="contactNo" class="form-label">Contact Number</label>
                                <input required type="number" ${disable} class="form-control" value=${user.username} id="contactNo">`
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

            document.getElementById('contactField').innerHTML += contactField;
            document.getElementById(formName).innerHTML += itemNameField + subCatField + catField;
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
              <label for="${field.fieldID}" class="form-label">${field.fieldName}</label>
              <br>`;

    var options = field.options.split(";");

    for (var option of options) {
        radioField +=
            `<label class="radio-inline" style="padding-right: 7px;" >
                        <input required class="form-check-input" type="radio" name="${field.fieldID}" value="${option}"> ${option}
                    </label>`;
    }

    radioField += `</div>`;

    document.getElementById(field.formName).innerHTML += radioField;
}

function buildText(field) {
    var textField = `<div class="col-md-6">
                        <label for="${field.fieldID}" class="form-label">${field.fieldName}</label>
                        <input required type="text" class="form-control" id="${field.fieldID}" placeholder="${field.placeholder ?? ""}">
                    </div>`;


    document.getElementById(field.formName).innerHTML += textField;
}

function buildNumber(field) {
    var numField = `<div class="col-md-6">
                        <label for="${field.fieldID}" class="form-label">${field.fieldName}</label>
                        <input required type="number" class="form-control" id="${field.fieldID}" placeholder="${field.placeholder ?? ""}">
                    </div>`;


    document.getElementById(field.formName).innerHTML += numField;
}

function buildFile(field) {
    var fileField = `<div class="col-6">
                        <div class="form-group">
                            <label for="${field.fieldID}" class="form-label">${field.fieldName}</label>
                            <input required type="file" class="form-control-file" id="${field.fieldID}" style="display:block">
                        </div>
                    </div>`;

    document.getElementById(field.formName).innerHTML += fileField;
}

function buildDropdown(field) {
    var dropdownField = `
            <div class="col-6">
              <label for="${field.fieldID}" class="form-label">${field.fieldName}</label>
              <select required class="form-select" id="${field.fieldID}">`;

    if (field.options !== null) {
        var options = field.options.split(";");
        for (var option of options) {
            dropdownField += `<option value="${option}"> ${option}</option>`;
        }
    }

    dropdownField += `</select></div>`;

    document.getElementById(field.formName).innerHTML += dropdownField;
}

function buildCheckbox(field) {

    var checkboxField = `
            <div class="col-6">
              <label for="${field.fieldID}" class="form-label">${field.fieldName}</label>
              <br>`;

    var options = field.options.split(";");

    var optionNo = 1;
    for (var option of options) {
        checkboxField +=
            `<input id="${field.fieldID}-${optionNo}" class="form-check-input" type="checkbox" name="${field.fieldID}" value="${option}">
                    <label for="${field.fieldID}-${optionNo}" class="form-check-inline" style="padding-right: 7px;" >${option}</label>`;
        optionNo++;
    }

    checkboxField += `</div>`;

    document.getElementById(field.formName).innerHTML += checkboxField;
}

// add edit icons to each field
function addIcons(formName) {
    $(`#${formName}`).find('input, select').each(function () {
        var fieldID = $(this).attr("name");
        if (fieldID === undefined) {
            fieldID = $(this).attr("id");
        }
        var editIcon = ` <i type="button" onclick="editField(${fieldID})" class="bi bi-pencil m-1" style="font-size:14px"></i>`;
        var label = $(`label[for="${fieldID}"]`);
        if (!label.next().is("i")) {
            label.after(editIcon);
        }
    });
};
//#endregion

// POPULATING ITEM CATEGORIES, SUB-CATEGORIES AND NAMES DROPDOWN LISTS
//#region
function checkLogin() {

    if (sessionStorage.getItem("user") != null) {
        user = JSON.parse(sessionStorage.getItem("user"))

        document.getElementById("loginLogoutButton").innerText = "Logout"
    }
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
    var catalogTable = document.getElementById('catalogTable')
    getCatalog().then(function populateCatalog(result) {
        var catalogList = result

        // reset catalog on refresh
        catalogTable.innerHTML = `<tr>
                                <th>Category</th>
                                <th>Sub-Category</th>
                                <th>Item Name</th>
                            </tr>`

        for (ele in catalogList) {
            catalogTable.innerHTML += `
            <tr>
                <td>${catalogList[ele].category}</td>
                <td>${catalogList[ele].subCat}</td>
                <td>${catalogList[ele].itemName}</td>
            </tr>
            `
        }
    })

}

async function getCatalog() {
    let response = await fetch("http://127.0.0.1:5003/getCatalog")
    let res = await response.json()

    if (res.code == 200) {
        return res.items
    } else {
        alert(res.message)
    }
}

//#endregion

// functions in index.html
//#region
var user = ""
var reqItemArr = ""
var mainCarouselDisplay = document.getElementById("mainCarouselDisplay")
var wishListTable = document.getElementById('wishListTable')
var emptyWLDisplay = document.getElementById('emptyWLDisplay')

// DataList display
var catSearchList = document.getElementById('catSearchList')
var subCatList = document.getElementById('subCatList')

function checkLogin() {
  if (sessionStorage.getItem("user") != null) {
    user = JSON.parse(sessionStorage.getItem("user"))
    // console.log(JSON.parse(user))

    document.getElementById("loginLogoutButton").innerText = "Logout"
  }

  // Requested Item Check
  if (user != "") {
    checkRequestedItems().then(function updateReqArr(result) {
      reqItemArr = result
    })
  }

  // async to return promise and update carousel page with items 
  loadCarousel().then(function retrieveItems(result) {
    mainCarouselDisplay.innerHTML = ""
    console.log(result)
    console.log(reqItemArr)
    if (result == "Empty") {
      mainCarouselDisplay.innerHTML =
        "<div class='text-center alert alert-warning rounded-3' style='height: 120px'> <p class='mt-3'> There are no items available for request at the moment, please try again later </p> </div>"
    } else {
      var donationItemList = result
      let itemCheck = []
      for (i in donationItemList) {
        // variable to check if donation has items, if no items smaller than expiry date, display another div instead
        date = new Date(donationItemList[i].timeSubmitted);
        lastDate = date.setDate(date.getDate() + 1);
        dateNow = Date.now();
        // if current date is earlier/smaller than expiry date
        if ((dateNow - lastDate) < 0) {
          itemCheck.push(donationItemList[i])
          var req = "Request!";
          var disable = "";
          if (reqItemArr.indexOf(donationItemList[i].donationID) != -1) {
            req = "Requested!";
            disable = "disabled";
          }

          if (itemCheck.length > 0) {
            mainCarouselDisplay.innerHTML += `
                                <div class="col-lg-4 d-flex align-items-stretch p-3 rounded-2">
                                <div class="card" style="width: 20rem;">
                                    <img src="./assets/img/donations/${donationItemList[i]["Item Photo"]}" class="card-img-top" alt="...">
                                    <div class="card-content">
                                    <div class="card-body">
                                        <h4 class="card-title">Item Name: ${donationItemList[i].itemName}</h4>
                                        <h6 class="card-subtitle mb-2">Category: ${donationItemList[i].category}</h6>
                                        <h6 class="card-subtitle">Sub-Category: ${donationItemList[i].subCat}</h6>
                                        <button data-tip="${donationItemList[i].donationID}" onclick="checkUserType(this)" ${disable} class="btn btn-primary">${req}</button>
                                    </div>
                                    </div>
                                </div>
                                </div>
                            `

          } else {
            mainCarouselDisplay.innerHTML =
              "<div class='text-center alert alert-warning rounded-3' style='height: 120px'> <p class='mt-3'> There are no items available for request at the moment, please try again later </p> </div>"
          }
        }
      }
      if (mainCarouselDisplay.innerHTML == "") {
        mainCarouselDisplay.innerHTML =
          "<div class='text-center alert alert-warning rounded-3' style='height: 120px'> <p class='mt-3'> There are no items available for request at the moment, please try again later </p> </div>"
      }
    }

  })

  // Function to retrieve Categories for dropdown
  getDropDownCat().then(function autoPopCategories(result) {
    var catList = result

    // reset search fields
    catSearchList.innerHTML = ""

    subCatList.innerHTML = ""

    // Add a default empty selection
    catSearchList.innerHTML = "<option selected> </option>"

    for (cat of catList) {
      catSearchList.innerHTML += `
                    <option value="${cat}">${cat}</option>
                `
    }
  })
}

// Function to load donations
async function loadCarousel() {
  try {
    let response = await fetch("http://127.0.0.1:5003/donation")
    let responseCode = await response.json()
    if (responseCode.code == 200) {
      return responseCode.data.items
    } else {
      return "Empty"
    }
  } catch (error) {
    alert(error)
  }
}

// Async function for Search Dropdown (Index Page)
async function getDropDownCat() {
  let response = await fetch("http://127.0.0.1:5003/getCat")
  let responseCode = await response.json()

  if (responseCode.code == 200) {
    return responseCode.data.categories
  } else {
    alert(responseCode.message)
  }
}

async function populateSubCat(cat) {
  subCatList.innerHTML = ""
  cat = cat.value
  let response = await fetch("http://127.0.0.1:5003/getSubCat/" + cat)
  let responseCode = await response.json()

  if (responseCode.code == 200) {
    subCatList.innerHTML += "<option selected> </option>"
    let subCatArr = []
    for (subcat of responseCode.data.subcats) {
      if (!subCatArr.includes(subcat.subCat)) {
        subCatArr.push(subcat.subCat)
      }
    }
    for (sub of subCatArr) {
      subCatList.innerHTML += `<option value="${sub}">${sub}</option>`
    }
  }
}

async function checkRequestedItems() {
  let response = await fetch("http://127.0.0.1:5003/request/" + user.username)
  let data = await response.json()
  if (data.code == 200) {
    return data.requestedItemIds
  }
}

function refreshpage() {
  window.location.reload()
}

function loginLogout() {
  if (document.getElementById("loginLogoutButton").innerText === "Login") {
    window.location.href = "login.html"
  } else {
    // user = ""
    sessionStorage.removeItem("user")
    window.location.reload()
  }
}

// Search function on Cat & Sub Cat once Sub Cat is selected
async function filter() {
  let subCatVal = subCatList.value

  let response = await fetch("http://127.0.0.1:5003/getItemsBySubCat/" + subCatVal)
  let responseCode = await response.json()

  if (responseCode.code == 200) {
    mainCarouselDisplay.innerHTML = ""
    let itemCheck = []
    for (item of responseCode.data.items) {
      console.log(item)
      date = new Date(item.timeSubmitted);
      lastDate = date.setDate(date.getDate() + 1);
      dateNow = Date.now();
      // if current date is earlier/smaller than expiry date
      if ((dateNow - lastDate) < 0) {
        itemCheck.push(item)

        if (itemCheck.length > 0) {
          var req = "Request!";
          var disable = "";
          if (reqItemArr.indexOf(item.donationID) != -1) {
            var req = "Requested!";
            var disable = "disabled";
          }

          mainCarouselDisplay.innerHTML += `
                            <div class="col-lg-4 d-flex align-items-stretch p-3 rounded-2">
                            <div class="card" style="width: 20rem;">
                                <img src="./assets/img/donations/${item["Item Photo"]}" class="card-img-top" alt="...">
                                <div class="card-content">
                                <div class="card-body">
                                    <h4 class="card-title">Item Name: ${item.itemName}</h5>
                                    <h6 class="card-subtitle mb-2">Category: ${item.category}</h6>
                                    <h6 class="card-subtitle">Sub-Category: ${item.subCat}</h6>
                                    <button data-tip="${item.donationID}" onclick="checkUserType(this)" ${disable} class="btn btn-primary">${req}</button>
                                </div>
                                </div>
                            </div>
                            </div>
                        `
        } else {
          mainCarouselDisplay.innerHTML =
            "<div class='text-center alert alert-warning rounded-3' style='height: 120px'> <p class='mt-3'> There are no items available for request at the moment, please try again later </p> </div>"
        }
      }
    }
  } else {
    mainCarouselDisplay.innerHTML =
      "<div class='text-center alert alert-warning rounded-3' style='height: 120px'> <p class='mt-3'> There are no items available for request at the moment, please try again later </p> </div>"
  }
}

function checkUserType(x) {
  var itemData = x.getAttribute("data-tip")

  if (user == "") {
    let confirmMsg = confirm(
      "Only Migrant Workers who are logged in are able to request for items, click 'Ok' to go to the Login Page.")

    if (confirmMsg == true) {
      window.location.href = "login.html"
    }

  } else if (user.userType == "worker") {
    if (dateNow - lastDate < 0) {
      window.location.href =
        `requestItemPage.html?id=${itemData}` // pass itemId over to request page to retrieve full item info
    } else {
      alert("This item has expired. Please refresh the page to see the list of items available.")
    }
    // console.log(itemData)
  }
}

//#endregion

// functions in submitting form page (donation)
// #region
retrieveForm('donation');

// can move to a common folder if every page uses?
function loginLogout() {
    if (document.getElementById("loginLogoutButton").innerText === "Login") {
        window.location.href = "login.html"
    } else {
        window.sessionStorage.removeItem("userType")
        window.location.reload()
    }
}

// #endregion

// functions to submit forms
// #region
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

    addDonation(formData, 'http://127.0.0.1:5003/formanswers')
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

// #endregion