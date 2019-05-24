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

function submit_interview(resume_id, post_id, status_value, table) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/api/interviews/");
  xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
  var csrftoken = getCookie('csrftoken');

  xhr.setRequestHeader("X-CSRFToken", csrftoken);

  data = {"resume": resume_id,
          "post": post_id,
          "is_active":true,
          "status": status_value,
          "result":"Pending",
         };

  console.log(data);
  xhr.onloadend = function() {
    //done
    table.draw();
  };

  xhr.send(JSON.stringify(data));
}

$(document).ready(function() {

  //$('.collapse').collapse();

  var resumes_selected = [];
  var post_selected = false;
  var post_selected_value = 0;
  var resume_selected = false;
  var resume_selected_value = 0;

  var table = $('#dataTable_resume').DataTable({
    "processing": true,
    "serverSide": true,

    "ajax": {
      "url": "/api/resumes/",
      "type": "GET",
      "data": function (d) {
        d.degree_id = $('#degree_id').val();
        d.age_id = $('#age_id').val();
        d.gender_id = $('#gender_id').val();
        d.post_id = post_selected_value;
      },
    },

    "rowCallback": function(row, data) {
      if ($.inArray(data.DT_RowId.toString(), resumes_selected) !== -1 ) {
        $(row).addClass('selected');
      }

    },

    "columns": [
      {"data": null,
       "visible": false,
       "checkboxes": {
       },
      },
      {"data": "candidate_id",
       "visible": false},
      {"data": "id"},
      {"data": "username"},
      {"data": "gender"},
      {"data": "age"},
      {"data": "phone_number"},
      {"data": "email"},
      {"data": "school"},
      {"data": "degree"},
      {"data": "major"},

      {"data": "is_match",
       render: function(data, type, row, meta) {
         if (row.is_match == 1) {
           return "Match"
         } else if (row.is_match == 0){
           return "Not Match"
         } else {
           // For default
           return "Match"
         }
       }},
      {"data": "interview_status_name"},

      /* ================================================================================ */
      {"data": "interview_status",
       render: function(data, type, row, meta) {

         /* -------------------------------------------------------------------------------- */
         if (row.interview_status == 0) {
           return `
<button class="invite_button btn btn-success border-0" data-toggle="modal" data-target="#inviteModal" id="` + row.id + `">
  <span class="text">AI </span>
</button>

<button class="invite_button btn btn-success border-0" id="` + row.id + `">
  <span class="text">SMS</span>
</button>

`;
         }
         /* -------------------------------------------------------------------------------- */
         else if (row.interview_status == 1) {
           return `
<button class="dial_button btn btn-success border-0" data-toggle="modal" data-target="#dialModal" id="` + row.id + `">
  <span class="text">Dial</span>
</button>
`;
         } else {
           return "Not yet";
         }
       }},
    ],
  });

  var table_post = $('#dataTable_post').DataTable({
    "lengthChange": false,
    "pageLength" : 5,

    "processing": true,
    "serverSide": true,

    "ajax": {
      "url": "/api/posts/",
      "type": "GET",
    },

    "rowCallback": function(row, data) {

      if ((post_selected === true) && (data.DT_RowId == post_selected_value)) {
        $(row).addClass('selected');
      }
    },

    "columns": [
      {"data": "id"},
      {"data": "department.company.name"},
      {"data": "department.name"},
      {"data": "name"},
    ],
  });

  $('#age_id').keyup(function() {
    table.draw();
  });

  $('#degree_id, #gender_id').change(function() {
    table.draw();
  });

  // resume table
  $('#dataTable_resume tbody').on('click', 'tr', function(e) {
    if (post_selected == false) {
      alert("Please select Post first.");
      e.stopPropagation();
    }

  });
  /*
    $('#dataTable tbody').on('click', 'tr', function() {
    var id = this.id;
    var index = $.inArray(id, resumes_selected);

    if ( index === -1 ) {
    resumes_selected.push(id);
    } else {
    resumes_selected.splice(index, 1);
    }

    $(this).toggleClass('selected');
    });
  */

  $(document).on('click', '.invite_button', function() {
    resume_selected_value = Number(this.id);
  });

  // post table
  $('#dataTable_post tbody').on('click', 'tr', function() {
    var id = this.id;

    if (id === post_selected_value && post_selected === true) {
      $(this).toggleClass('selected');
      post_selected = false;
    } else {
      $(this).toggleClass('selected');

      if (post_selected === true) {
        $('tr#' + post_selected_value).toggleClass('selected');
      }
      post_selected = true;
      post_selected_value = id;

      var tr = document.getElementById(id);
      table.draw();

      document.getElementById("text_company_name").innerHTML = tr.innerText;
    }
  });

  $('#id_button_submit').on('click', function() {
    // submit to interview interface
    /*
    for (var i = 0; i < resumes_selected.length; i++) {
      submit_interview(Number(resumes_selected[i], Number(post_selected_value)), table);
    }
    */
  });

  $(function(){
    $('#inviteFormSubmit').click(function(e){
      e.preventDefault();
      var resume_id = resume_selected_value;
      var post_id = post_selected_value;
      var status = 1;

      alert("Resume:" + resume_id + " :Post:" + post_id);
      $('#inviteModal').modal('hide');
      //$('#formResults').text($('#myForm').serialize());
      submit_interview(resume_id, post_id, status, table);
      /*
        $.post('http://path/to/post',
        $('#myForm').serialize(),
        function(data, status, xhr){
        // do something here with response;
        });
      */
    });
  });

});
