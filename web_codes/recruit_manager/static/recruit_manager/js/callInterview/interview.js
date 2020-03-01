var resumeId = -1
var projectId = -1
var interviewId = -1
var experience_id = -1
var on_experience_add = false
var exp_map = {}

$(document).ready(function() {
    resumeId = $('#resumeInfo').attr('resumeId')
    projectId = $('#resumeInfo').attr('projectId')
    interviewId = $('#resumeInfo').attr('interviewId')
    console.log("basicInfo resumeId(",
            resumeId, ") projectId(",
            projectId, ") interviewId(",
            interviewId, ")")
    GetResumeTag()
});

function InsertTag(ele) {
    var tagInfo = '<span style="border: 2px solid #E8E8E8">' + ele.tag + '</span>'
    $('#userTagPanel').append(tagInfo)
}

$(document).on('click', '#userTagAddButton', function() {
    var tagname = $('#userNewTag').val()
    var data = {
        "resume": resumeId,
        "tag": tagname,
    }
    console.log("tagname", tagname)
	xhr_common_send('POST', '/api/tags/', data, function(response) {
        console.log("post successfully")
        $('#userNewTag').val("")
        GetResumeTag()
	})

});

function GetResumeTag() {
    document.getElementById('userTagPanel').innerHTML = ""
	xhr_common_send('GET', '/api/tags/?resume_id=' + resumeId , null, function(response) {
        console.log("-------------", response)
        $.each(response.results, function(index, ele) {
            console.log("insert ", ele.id, " ", ele.tagname, "")
            InsertTag(ele)
        });
	});
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
