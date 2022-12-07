function enableNext(input) {
    var btn = document.getElementById('next_button_box');
    btn.style.display = 'block';
    console.log("yieskhrjgm,")
  }

function enableSubmit(input) {
    var btn = document.getElementById('submit_button_box');
    btn.style.display = 'block';
  }

function readURL(input) {
       if (input.files && input.files[0]) {
           var reader = new FileReader();
           reader.onload = function (e) {
               $('#user_image')
                   .attr('src', e.target.result)
                   .width(150)
                   .height(200);
           };
           reader.readAsDataURL(input.files[0]);
           var img = document.getElementById('user_image');
           img.style.display = 'block';
       }
   }

function showInputFields(input) {
    var user_input = document.getElementById('user_input_div');
    var next_button = document.getElementById('next_button');
    var user_address = document.getElementById('user_address_div');
    user_input.style.display = 'none';
    next_button.style.display = 'none';
    user_address.style.display = 'block';
    
   }

var dataURLToBlob = function(dataURL) {
    var BASE64_MARKER = ';base64,';
    if (dataURL.indexOf(BASE64_MARKER) == -1) {
        var parts = dataURL.split(',');
        var contentType = parts[0].split(':')[1];
        var raw = parts[1];

        return new Blob([raw], {type: contentType});
    }

    var parts = dataURL.split(BASE64_MARKER);
    var contentType = parts[0].split(':')[1];
    var raw = window.atob(parts[1]);
    var rawLength = raw.length;

    var uInt8Array = new Uint8Array(rawLength);

    for (var i = 0; i < rawLength; ++i) {
        uInt8Array[i] = raw.charCodeAt(i);
    }

    return new Blob([uInt8Array], {type: contentType});
}

let imgupload = document.getElementById('img_file');
imgupload.addEventListener('change', function (e) {
    if (e.target.files) {
        let imageVal = e.target.files[0];
        var reader = new FileReader();
        reader.onload = function (e) {
            var img = document.createElement("img");
            img.onload = function (event) {
                // This line is dynamically creating a canvas element
                var canvas = document.createElement("canvas");
                
                const MAX_WIDTH = 200;
                const scaleSize = MAX_WIDTH / event.target.width;
                canvas.width = MAX_WIDTH;
                canvas.height = event.target.height * scaleSize;                
                var ctx = canvas.getContext("2d");

                //This line shows the actual resizing of image
                ctx.drawImage(event.target, 0, 0, canvas.width, canvas.height);
                
                //This line is used to display the resized image in the body
                const srcEncoded = ctx.canvas.toDataURL(event.target, 'image/jpeg')
                // var url = canvas.toDataURL(imageVal.type);
                var user_image = document.getElementById("user_image")
                user_image.src = srcEncoded;
                user_image.style.display = 'block';
                var resizedImage = dataURLToBlob(srcEncoded);
                var data = new FormData($("form[id*='imgForm']")[0]);
                if (event.blob && event.srcEncoded) {
                    data.append('image', event.blob);
                }
            }
            img.src = e.target.result;
        }
        reader.readAsDataURL(imageVal);
    }
});



const myForm = document.getElementById('imgForm');
let loader = document.getElementById('loader');

if (myForm !== null) {
  myForm.addEventListener('submit', function (event) {
    loader.style.display = 'block';
  });
}

function show_student(){
  document.getElementById("employee").style.display = 'none';
  document.getElementById("student").style.display = 'block';

  document.getElementById("comp_name").required = false;
  document.getElementById("designation").required = false;

  document.getElementById("insti_name").required = true;
  document.getElementById("ed_year").required = true;
}

function show_employee(){
  document.getElementById("student").style.display = 'none';
  document.getElementById("employee").style.display = 'block';

  document.getElementById("comp_name").required = true;
  document.getElementById("designation").required = true;

  document.getElementById("insti_name").required = false;
  document.getElementById("ed_year").required = false;
}