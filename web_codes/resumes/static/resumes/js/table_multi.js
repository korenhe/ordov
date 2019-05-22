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

function submit_interview(resume_id, post_id, table) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/api/interviews/");
  xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
  var csrftoken = getCookie('csrftoken');

  xhr.setRequestHeader("X-CSRFToken", csrftoken);

  data = {"resume": resume_id,
          "post": post_id,
          "is_active":true,
          "status": 0,
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

  var resume_selected = [];
  var post_selected = false;
  var post_selected_value = 0;

  var table = $('#dataTable').DataTable({
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
      if ($.inArray(data.DT_RowId.toString(), resume_selected) !== -1 ) {
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
      {"data": "is_in_interview",
       render: function(data, type, row, meta) {
         if (row.is_in_interview) {
           return `TRUE`;
         } else {
           return `
<button class="xxbutton btn btn-success btn-icon-split border-0" id="` + row.id + `">
  <span class="icon text-white-50">
    <i class="fas fa-check"></i></span>
  <span class="text">简历符合并邀约</span>
</button>

<button class="btn btn-success btn-icon-split border-0" id="stage">
  <span class="icon text-white-50">
    <i class="fas fa-check"></i></span>
  <span class="text">简历不符合</span>
</button>
`;
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

  $('#dataTable tbody').on('click', 'tr', function() {
    table.draw();
  });
  /*
    $('#dataTable tbody').on('click', 'tr', function() {
    var id = this.id;
    var index = $.inArray(id, resume_selected);

    if ( index === -1 ) {
    resume_selected.push(id);
    } else {
    resume_selected.splice(index, 1);
    }

    $(this).toggleClass('selected');
    });
  */

  $(document).on('click', '.xxbutton', function() {
    submit_interview(Number(this.id), post_selected_value, table);
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
    console.log(post_selected_value);
    console.log(resume_selected);

    // submit to interview interface
    for (var i = 0; i < resume_selected.length; i++) {
      submit_interview(Number(resume_selected[i], Number(post_selected_value)), table);
    }
  });
});
