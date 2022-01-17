var userType = ""
var itemCategoryOptions = document.getElementById('itemCategoryOptions')
var itemNameOptions = document.getElementById("itemNameOptions")

function checkLogin() {

    getDropDownCat().then(function autoPopCategories(result) {
            var catList = result
            // reset dropdown fields
            itemCategoryOptions.innerHTML = "";
            itemNameOptions.innerHTML = "";
            // Start off with an empty selected option for category
            itemCategoryOptions.innerHTML += `<option selected> </option>`

            for (cat of catList) {
                itemCategoryOptions.innerHTML += `
                <option value="${cat}">${cat}</option>
            `
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
    itemNameOptions.innerHTML = ""
    cat = cat.value
    let response = await fetch("http://127.0.0.1:5004/getItemsInCat/" + cat)
    let responseCode = await response.json()

    if (responseCode.code == 200) {
        itemNameOptions.innerHTML += "<option selected> </option>"
        for (cat of responseCode.data.itemsInCat) {
            itemNameOptions.innerHTML += `<option>${cat.itemName}</option>`
        }
    }
}

const form = document.getElementById("donateForm")

form.addEventListener("submit", (event) => {
    event.preventDefault();

    var donateFormElements = document.forms[0].elements

    // console.log(donateFormElements)

    for (i in donateFormElements) {
        console.log(donateFormElements[i].value)
    }
})

// Example POST method implementation:
async function addDonation(url = 'http://127.0.0.1:5004/addDonation', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
}

function loginLogout() {
    if (document.getElementById("loginLogoutButton").innerText === "Login") {
        window.location.href = "login.html"
    } else {
        window.sessionStorage.removeItem("userType")
        window.location.reload()
    }
}
// var itemCategoryOptions = document.getElementById('itemCategory')

// $(async() => { 
// var serviceURL = 'http://127.0.0.1:5000/getCat';
// try {
//       const response =
//       await fetch(
//         serviceURL, { method: 'GET' }
//       );
//       const result = await response.json();
//       if (response.ok) {
//           var categories = result.data;
//           var categoryDropdown = '';
//           console.log(categories);
//           for (const name of categories){
//             categoryDropdown += "<option value=" + name.attachedcategory + ">" + name.attachedcategory +"</option>" ;
//           }
//           document.getElementById("itemCategory").innerHTML= categoryDropdown;  
//         }
//       } catch (error) {
//       showError
//       ('There is a problem retrieving category name. Please try again later.' + error);
//         } 
//     }
// );

// $(async() => { 
//   var serviceURL = 'http://127.0.0.1:5000/getItemsInCat/' + itemCategoryOptions;
//   try {
//         const response =
//         await fetch(
//           serviceURL, { method: 'GET' }
//         );
//         const result = await response.json();
//         if (response.ok) {
//             var itemName = result.data;
//             var itemNameDropdown = '';
//             console.log(categories);
//             for (const name of itemName){
//               itemNameDropdown += "<option value=" + name.itemname + ">" + name.itemname +"</option>" ;
//             }
//             document.getElementById("itemName").innerHTML= itemNameDropdown;  
//           }
//         } catch (error) {
//         showError
//         ('There is a problem retrieving item name. Please try again later.' + error);
//           } 
//       }
//   );





// editing part NOT DONE 
async function addInputField(){
  var labelName = document.getElementById('newLabel').innerHTML;
  var field = document.getElementById('input').innerHTML;

  console.log(field);
  console.log(labelName);

  if (field == 'text'){
    $('#donorForm').append('<div class="col-md-6"> <label class="form-label">' + labelName +
    '</label> <input type="text" class="form-control" '+ 'id="' + labelName 
    + '"placeholder="Enter '+ labelName + '"> </div>)') ; 
  }
  else if (field == "Checkbox"){
    //technically this is wrong because i shouldnt usee textbox to represent the number but count the number of input they want like how y2 did it so the checkbox radio and dropdown will be the same
    $('#editForm').append('<div class="col-md-6"> <label class="form-label"> How many fields would you like ? </label> <input type="text" class="form-control" '+ 'id="fieldQty" > </div>)'+
    '<div class="col-12" style="text-align: right; color: #A57F60;"><button type="submit" class="btn btn-outline-light" id= "add-fieldQty" style="color:white; background-color: #A57F60;" onclick = "addCheckbox()">Add Num Qty Field</button></div>') ;
  }
  else if (field == "radio"){
    console.log("1")
  }
  else if (field == "Dropdown"){
    console.log("2")
  }
  else{
    //alert("Please choose a field type!");
    console.log("nt working")
  }


//   $('#quiz-portion').append(
//     "<div class='row mt-3 mb-3 qnsblock' id='question-block" + qnscount.toString() + "'>" +
//         "<div class='card' style='padding-left: 0; padding-right: 0;''>" +
//             "<div class='card-header'>" +
//                 "<label for='Question'>Question:</label>" +
//                 "<textarea class='form-control allqns' id='Question" + qnscount.toString() + "' rows='3' ></textarea>" +
//                 "<label for='Answer'>Answer:</label>" +
//                 "<textarea class='form-control allans' id='Answer" + qnscount.toString() + "' rows='3' ></textarea>" +
//             "</div>" +
//             "<div class='card-body'>" +
//                 "<div class='dropdown'>" +
//                     "<select class='custom-select col-5' id='selectquiztype" + qnscount.toString() + "' onchange='showQnsType(this.id)'>" +
//                         "<option selected>Select Quiz Type</option>" +
//                         "<option value='T/F'>True/False (T/F)</option>" +
//                         "<option value='MCQ'>Multiple Choice Question (MCQ)</option>" +
//                     "</select>" + 
//                     "<div class='row ml-4 mt-2' id='showqnstype" + qnscount.toString() + "'>" +
//                         "<div id='qnstype" + qnscount.toString() + "'></div>" +
//                     "</div>" +
//                 "</div>" +
//                 "<div>" +
//                     "<button class='col-sm-5 btn btn-outline-secondary' type='button' id='add-qns" + qnscount.toString() + "' onclick='deleteQuestion(this.id)'>Delete Question</button>" +
//                 "</div>" +
//             "</div>" +
//         "</div>" +
//     "</div>" 
// )

}

function addCheckbox(){
  //should be a number 
  var fieldQty = document.getElementById('add-fieldQty').innerHTML;
  var num = 0;
  while (num < fieldQty){

  }
  
}


function save(){

}

