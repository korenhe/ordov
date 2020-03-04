var resumeId = -1
var projectId = -1
var interviewId = -1

$(document).ready(function() {
    resumeId = $('#resumeInfo').attr('resumeId')
    projectId = $('#resumeInfo').attr('projectId')
    interviewId = $('#resumeInfo').attr('interviewId')
    console.log("basicInfo resumeId(",
            resumeId, ") projectId(",
            projectId, ") interviewId(",
            interviewId, ")")
});

$(document).on('click', '#deepContactButton', function() {
    var status = 2; 
    //submitInterviewById(interviewId, "/api/interviews/", status, '深度沟通');
});

$(document).on('click', '#unlinkButton', function() {
	var status = 2;
	//submitInterviewById(interviewId, "/api/interviews/", status, '未接通');
});

$(document).on('click', '#agreeInterviewButton', function() {
});

$(document).on('click', '#giveupInterviewButton', function() {
});


function submitInterviewById(interviewId, url, status_value, sub_status) {
  data = {"is_active":true,
          "status": status_value,
          "post": post_selected_value,
          "result":"Pending",
          "sub_status":sub_status,
         };

  xhr_common_send("PATCH", url + interview_id + '/', data);
}

//====================================
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

