var form = document.getElementById("signupform");
var thankyou = document.getElementById('thankyou');
var errorblock = document.getElementById('error');

form.onsubmit = function (e) {
  // stop the regular form submission
  e.preventDefault();

  // collect the form data while iterating over the inputs
  var data = {};
  for (var i = 0, ii = form.length; i < ii; ++i) {
    var input = form[i];
    if (input.name) {
      data[input.name] = input.value;
    }
  }

  if (data['name'] == "") {
    alert("Please tell us what's your name?");
  } else {
    var name=data['name'].split(" ");
    data['first_name'] = name[0]
    data['last_name'] = name[1] ? name[1] : ""
  }

  if (data['email'] == "") {
    alert("Please enter a valid email address");
  } else if(data['country'] == "") {
	  alert("Please select a country");
  } else {
    // construct an HTTP request
    var xhr = new XMLHttpRequest();
    xhr.open(form.method, form.action, true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.setRequestHeader('Authorization', data['g-recaptcha-response'])

    // send the collected data as JSON
    console.log(data);
    xhr.send(JSON.stringify(data));

    xhr.onerror = function () {
      console.log(this);
      popup.style.display = "table"
      errorblock.style.display = "block";
    };

    xhr.onload = function () {
      console.log(this);
      if (this.status < 400) {
        popup.style.display = "table"
        thankyou.style.display = "block";
      } else {
        popup.style.display = "table"
        errorblock.style.display = "block";
      }
    };
  }
};

function enableBtn(){
  var btnSignUp = document.getElementById("btnSignUp");

  btnSignUp.disabled = false;
  btnSignUp.style.color="white";
  btnSignUp.style.background="#ff9212";
}