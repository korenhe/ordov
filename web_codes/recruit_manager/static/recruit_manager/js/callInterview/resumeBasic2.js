var resumeId = -1
var experience_id = -1
var on_experience_add = false
var exp_map = {}

$(document).ready(function() {
    resumeId = $('#resumeInfo').attr('resumeId')
    console.log("basicInfo resumeId(", resumeId, ")")
});

$(document).on('click', '#userBasicEditButton', function() {

    GetBasicInfo()
    $('#userBasicHeader').css('background-color', '#66FFFF')
    $('#userBasicEditPanel').css('display', 'block') // Attention here: block not inline
    $('#userBasicShowPanel').css('display', 'none')

    $('#userBasicEditButton').css('display', 'none')
    $('#userBasicSaveButton').css('display', 'inline')
});

$(document).on('click', '#userBasicSaveButton', function() {

    UpdateBasicInfo()
    $('#userBasicHeader').css('background-color', '#FFFFFF')
    $('#userBasicEditPanel').css('display', 'none')
    $('#userBasicShowPanel').css('display', 'block')

    $('#userBasicEditButton').css('display', 'inline')
    $('#userBasicSaveButton').css('display', 'none')

    GetBasicInfo()
});

function GetBasicInfo() {
	xhr_common_send('GET', '/api/resumes/' + resumeId + '/', null, function(response) {
      console.log(response)
      gender = '男'
      if (response.gender == 'f') {
          gender = '女'
      }

      // Update the show panel info
      $('#userBasicShowName').val(response.username)
      $('#userBasicShowGendor').val(gender)
      $('#userBasicShowAge').val("")
      $('#userBasicShowDegree').val("")
      $('#userBasicShowGraduate').val(response.birthorigin)
      $('#userBasicShowCurResidence').val("xiaoming")
      $('#userBasicShowBirthPlace').val(response.phone_number)

      // Update the edit panel info
      $('#userBasicEditName').val(response.username)
      $('#userBasicEditGendor').val(gender)
      $('#userBasicEditAge').val("")
      $('#userBasicEditDegree').val("")
      $('#userBasicEditGraduate').val(response.birthorigin)
      $('#userBasicEditCurResidence').val("xiaoming")
      $('#userBasicEditBirthPlace').val(response.phone_number)
	})
}

function UpdateBasicInfo() {
    // Parsing the basic info and update
    var data = {
      "username": $('#userBasicEditName').val(),
      "gender": 'f',
      "age": 34,
      "degree": 3,
      "graduate": $('#userBasicEditGraduate').val(),
      "brith_place": $('#userBasicEditBirthPlace').val(),
    }
    console.log("data:", data)
	xhr_common_send('PUT', '/api/resumes/' + resumeId + '/', data, function(response){
		console.log("success")
	})
}

// Meta Function
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1)); 
        break;
      }    
    }    
  }
  return cookieValue;
}

function xhr_common_send(method, url, data, succCallback=null) {
  var xhr = new XMLHttpRequest();
  xhr.open(method, url);

  xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

  var csrftoken = getCookie('csrftoken');

  xhr.setRequestHeader("X-CSRFToken", csrftoken);
  console.log("------------------------------------>")

  xhr.onreadystatechange=function() {
    if (xhr.readyState === 4){ //if complete
      // 2xx is ok, ref: https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
      if(xhr.status >= 200 && xhr.status < 300) {
        if (succCallback) {
          succCallback(JSON.parse(xhr.response))
        }
		console.log("success")
      } else {
        console.log("csrftoken: ", csrftoken)
        console.log(xhr.responseText)
        console.log(xhr.status)
        console.log(xhr.statusText)
        console.log(url)
        console.log(data)
        alert("Something error happend\n");
      }
    }
  }
  xhr.send(JSON.stringify(data));
}
