const myForm = document.getElementById('myForm');
let loader = document.getElementById('loader');

myForm.addEventListener('submit', function (event) {
  loader.style.display = 'block';
});

// let btn = document.querySelector('button');
// let prevVal = "";

// btn.addEventListener('click', function () {
//   // form submission starts
//   // button is disabled
//   btn.classList.remove('is-info');
//   btn.classList.add('is-loading');
  // btn.disabled = true;
  
  // This disables the whole form via the fieldset
//   btn.form.firstElementChild.disabled = true;
  
//   // this setTimeout call mimics some asyncronous action
//   // you would have something else here
//   window.setTimeout(function () {
//     // when asyncronous action is done, remove the spinner
//     // re-enable button/fieldset
//     btn.classList.remove('is-loading');
//     btn.disabled = false;
//     btn.form.firstElementChild.disabled = false;
//   }, 30000);
// }, false);

// document.querySelector('input').addEventListener('input', function(e){
//   if(this.checkValidity()){
//     prevVal = this.value;
//     // btn.disabled = true
//   } else {
//     this.value = prevVal;
//   }
// });
// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

// document.getElementById('submitbutton').disabled = !cansubmit;

function show_aadhaar(){
	document.getElementById("pan").style.display = 'none';
	document.getElementById("aadhaar").style.display = 'block';
}

function show_pan(){
	document.getElementById("aadhaar").style.display = 'none';
	document.getElementById("pan").style.display = 'block';
}

document.addEventListener('DOMContentLoaded', () => {
  (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
    const $notification = $delete.parentNode;

    $delete.addEventListener('click', () => {
      $notification.parentNode.removeChild($notification);
    });
  });
});

function filterTable(key) {
  var dict = {
    "User: Not Initiated": "pending",
    "User: In Progress": "in_progress",
    "Completed": "completed",
  };
  var table = document.getElementById('mytable');
  rows = table.getElementsByTagName("TR");
  let flag = false;

  for (let row of rows) {
    let cells = row.getElementsByTagName("TD");
    
    if (key.toUpperCase().includes("INVITED")) {
      if (cells[6].textContent.toUpperCase().includes("INVITE") || cells[6].textContent.toUpperCase().includes("ADD")) {
          flag = true;
      }
    } else {
      if (!cells[6].textContent.toUpperCase().includes("INVITE") && cells[4].textContent.toLowerCase().includes(dict[key])) {
        flag = true;
      }
    }

    if (flag) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }

    flag = false;
  }
} 
    
//create a user-defined function to download CSV file   
function download_csv_file() { 
  //create CSV file data in an array  
  var csvFileData = [  
     ['name', 'phone_number', 'email_id', 'uan'],
     ['John Doe', '+919876543210', 'johndoe@example.com', '11322234324242'],
  ];   
  csv = ''

  //merge the data with CSV  
  csvFileData.forEach(function(row) {  
    csv += row.join(',');
    csv += "\n";
  });
  //display the created CSV data on the web browser   
  // document.write('name,phone_number,email_id,uan');
  
     
  var hiddenElement = document.createElement('a');  
  hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);  
  hiddenElement.target = '_blank';  
      
  //provide the name for the CSV file to be downloaded  
  hiddenElement.download = 'candidates_details.csv';  
  hiddenElement.click();  
}  

function verify_candidate() {
  myform = document.getElementById('myForm');
  myform.action = "/verify_candidate";
  return false;
}
