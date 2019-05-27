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

$(document).ready(function() {

  //$('.collapse').collapse();

  var resumes_selected = [];
  var post_selected = false;
  var post_selected_value = 0;
  var resume_selected = false;
  var resume_selected_value = 0;
  var interview_selected_value = 0;
  var filter_status_value = 0;

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
        //var list_elements = document.getElementsByClassName("list-group-item active");
        d.status_id = filter_status_value;
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
      {"data": "interview_id", "visible": false},
      {"data": "candidate_id", "visible": false},
      {"data": "id"}, // resume id
      {"data": "username"},
      {"data": "gender", "visible":false},
      {"data": "age"},
      {"data": "phone_number", "visible":false},
      {"data": "email", "visible": false},
      {"data": "school", "visible": false},
      {"data": "degree"},
      {"data": "major"},

      {"data": "is_match",
       "orderable": false,
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
      {"data": "interview_status_name",
       "orderable": false
      },

      /* ================================================================================ */
      {"data": "interview_status",
       "orderable": false,
       render: function(data, type, row, meta) {

         /* -------------------------------------------------------------------------------- */
         if (row.interview_status == 0) {
           return `
                <button class="invite_button btn btn-success border-0" id="` + row.id + `" style="display:none;">
                <span class="text">不合适</span>
                </button>

                <select class="stage_zero_select form-control" id="` + row.id + `">
                    <option>待选状态</option>
                    <option>AI沟通</option>
                    <option>短信沟通</option>
                    <option>人工沟通</option>
                    <option>不合适</option>
                </select>
          `;
         }
         /* -------------------------------------------------------------------------------- */
         else if (row.interview_status == 1) {
           return `
               <!--
                <button class="dial_button btn btn-success border-0" data-toggle="modal" data-target="#dialModal" id="` + row.interview_id + `">
  <span class="text">打电话</span>
</button>
               -->
                <select class="stage_one_select form-control" id="` + row.interview_id + `">
                    <option>等待AI结果</option>
                    <option>继续下轮过程</option>
                    <option>终止面试</option>
                </select>

`;
         }
         /* -------------------------------------------------------------------------------- */
         else if (row.interview_status == 2) {
           return `
`;
         }
         /* -------------------------------------------------------------------------------- */
         else if (row.interview_status == 3) {
           return `
                <select class="stage_three_select form-control" id="` + row.interview_id + `" data-resume_id="` + row.id + `">
                    <option>面试过程中</option>
                    <option>查看职位信息</option>
                    <option>查看应聘者信息</option>
                    <option>SUCCESS:填写面试报告</option>
                    <option>FAIL:终止面试</option>
                </select>
`;
         }
         /* -------------------------------------------------------------------------------- */
         else if (row.interview_status == 4) {
           return `
<button class="entry_button btn btn-success border-0" data-toggle="modal" data-target="#entryModal" id="` + row.interview_id + `">
  <span class="text">入职</span>
</button>
`;
         }
         /* -------------------------------------------------------------------------------- */
         else if (row.interview_status == 5) {
           return `
<button class="inspect_button btn btn-success border-0" data-toggle="modal" data-target="#inspectModal" id="` + row.interview_id + `">
  <span class="text">考察期</span>
</button>
`;
         }
         /* -------------------------------------------------------------------------------- */
         else if (row.interview_status == 6) {
           return `
<button class="payback_button btn btn-success border-0" data-toggle="modal" data-target="#paybackModal" id="` + row.interview_id + `">
  <span class="text">入职反馈</span>
</button>
`;
         }
         /* -------------------------------------------------------------------------------- */
         else {
           return "流程结束";
         }
       }},
    ],
  });

  var table_post = $('#dataTable_post').DataTable({
    "lengthChange": false,
    "pageLength" : 15,
    "pagingType": "scrolling",
    "processing": false,
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
      {"data": "department.company.name"},
    ],
  });

  $('#age_id').keyup(function() {
    page_refresh(table);
  });

  $('.list-group-item').on('click', function(e) {
    filter_status_value = this.value;
    page_refresh(table);
  });

  $('#degree_id, #gender_id').change(function() {
    page_refresh(table);
  });

  // resume table
  $('#dataTable_resume tbody').on('click', 'tr', function(e) {
    if (post_selected == false) {
      alert("Please select Post first.");
      e.stopPropagation();
    }

  });

  function page_refresh(table) {
    // update statistic info
    var xx = t_resume_statistic_url;
    $.ajax({
      url: "/manager/resumes/statistic/" + post_selected_value + "/",
      type: 'GET',
      data: null,
      success: function(response) {
        document.getElementById("badge_statistic_stage_0").innerHTML = response.resumes_total;
        for (var i = 1; i < 8; i++) {
          document.getElementById("badge_statistic_stage_" + i).innerHTML = response.interviews_status_filters[i-1];
        }
      },
      error: function() {
        console.log("get statistic info failed");
      },
    });

    table.draw();
  }

  function stop_interview_by_id(interview_id, url, status_value, table) {
    var xhr = new XMLHttpRequest();
    xhr.open("PATCH", url + interview_id + '/');
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    var csrftoken = getCookie('csrftoken');

    xhr.setRequestHeader("X-CSRFToken", csrftoken);

    data = {
      "is_active":false,
      "status": status_value,
      "result":"Stop",
    };

    console.log(data);
    xhr.onloadend = function() {
      //done
      page_refresh(table);
    };

    xhr.send(JSON.stringify(data));
  }


  function submit_interview_by_id(interview_id, url, status_value, table) {
    var xhr = new XMLHttpRequest();
    xhr.open("PATCH", url + interview_id + '/');
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    var csrftoken = getCookie('csrftoken');

    xhr.setRequestHeader("X-CSRFToken", csrftoken);

    data = {
      "is_active":true,
      "status": status_value,
      "result":"Pending",
    };

    console.log(data);
    xhr.onloadend = function() {
      //done
      page_refresh(table);
    };

    xhr.send(JSON.stringify(data));
  }

  function submit_interview_by_compound(resume_id, post_id, url, status_value, table) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url);
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
      page_refresh(table);
    };

    xhr.send(JSON.stringify(data));
  }

  function show_post_modal(post_id) {
    $.ajax({
      url:'/api/posts/' + post_id + '/',
      type: 'GET',
      data: null,
      success: function(response) {

        /* here the abbreviation is not work, don't know why. Since the getElementbyid method is the most effience one, use it. */
        //$('#text_postinfo_company').value = response.department.company.name;
        //document.querySelector('#text_postinfo_company').value = response.department.company.name;
        document.getElementById("text_postinfo_company").value = response.department.company.name;
        document.getElementById("text_postinfo_department").value = response.department.name;
        document.getElementById("text_postinfo_post").value = response.name;
        document.getElementById("text_postinfo_description").value = response.description;

        $('#postModal').modal('toggle');
      },
      error: function() {
        console.log("get post info failed");
      },
    });
  }

  function show_resume_modal(resume_id) {
    $.ajax({
      url:'/api/resumes/' + resume_id + '/',
      type: 'GET',
      data: null,
      success: function(response) {

        document.getElementById("text_resumeinfo_username").value = response.username;
        document.getElementById("text_resumeinfo_degree").value = response.degree;
        document.getElementById("text_resumeinfo_school").value = response.school;
        document.getElementById("text_resumeinfo_phone_number").value = response.phone_number;

        $('#resumeModal').modal('toggle');
      },
      error: function() {
        console.log("get resume info failed");
      },
    });
  }

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
    alert(resume_selected_value)
  });

  // use 'click' here, otherwise, if user select 'next' and then closed, he should change to other stats then back to 'next' to trigger the event.
  $(document).on('click', '.stage_zero_select', function() {
	resume_selected_value = Number(this.id);

    /* Attention: how to select one item by variable */
    /*value = $(".stage_zero_select:eq("+(resume_selected_value-1)+")").val() */
    /* the intersection selector for jQuery */

    value = $("#"+(resume_selected_value)+".stage_zero_select").val()
    if (value == "AI沟通") {
       $('#dialModal').modal('toggle');
    } else if (value == "短信沟通") {
    } else if (value == "人工沟通") {
    } else if (value == "不符合要求") {
    }
  });

  $(document).on('click', '.stage_one_select', function() {
    interview_selected_value = Number(this.id);

    value = $("#"+(interview_selected_value)+".stage_one_select").val()
    if (value == "等待AI结果") {
    } else if (value == "继续下轮过程") {
        $('#nextModal').modal('toggle');
    } else if (value == "终止面试") {
        $('#stopModal').modal('toggle');
    }

  });

  $(document).on('click', '.stage_three_select', function() {
    interview_selected_value = Number(this.id);

    value = $("#"+(interview_selected_value)+".stage_three_select").val()
    if (value == "面试过程中") {
    } else if (value == "查看职位信息") {
      // show post
      show_post_modal(post_selected_value);
    } else if (value == "查看应聘者信息") {
      $('#resumeModal').modal('toggle');
      resume_id = this.dataset.resume_id;
      show_resume_modal(resume_id);
    } else if (value == "SUCCESS:填写面试报告") {
      $('#interviewModal2').modal('toggle');
    } else if (value == "FAIL:终止面试") {
      $('#stopModal').modal('toggle');
    }
  });

  $(document).on('click', '.dial_button', function() {
    interview_selected_value = Number(this.id);
  });

  $(document).on('click', '.interview_button', function() {
    interview_selected_value = Number(this.id);
  });

  $(document).on('click', '.offer_button', function() {
    interview_selected_value = Number(this.id);
  });

  $(document).on('click', '.entry_button', function() {
    interview_selected_value = Number(this.id);
  });

  $(document).on('click', '.inspect_button', function() {
    interview_selected_value = Number(this.id);
  });

  $(document).on('click', '.payback_button', function() {
    interview_selected_value = Number(this.id);
  });

  // post table
  $('#dataTable_post tbody').on('click', 'tr', function() {
    var id = this.id;

    if (id === post_selected_value && post_selected === true) {
      $(this).toggleClass('selected');
      post_selected = false;

      document.getElementById("text_company_name").innerHTML = "选择要操作的岗位";
    } else {
      $(this).toggleClass('selected');

      if (post_selected === true) {
        $('tr#' + post_selected_value).toggleClass('selected');
      }
      post_selected = true;
      post_selected_value = id;

      var tr = document.getElementById(id);
      page_refresh(table);

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
      submit_interview_by_compound(resume_id, post_id, "/api/interviews/", status, table);
      /*
        $.post('http://path/to/post',
        $('#myForm').serialize(),
        function(data, status, xhr){
        // do something here with response;
        });
      */
    });
  });

  $(function(){
    $('#dialFormSubmit').click(function(e){
      e.preventDefault();
      var resume_id = resume_selected_value;
      var post_id = post_selected_value;
      var status = 1;

      $('#dialModal').modal('hide');
      submit_interview_by_compound(resume_id, post_id, "/api/interviews/", status, table);
    });
  });

  $(function() {
    $('#stopFormSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#stopModal').modal('hide');
      var status = -1 // current status, not updated

      stop_interview_by_id(interview_id, "/api/interviews/", status, table);
    });
  });

  $(function() {
    $('#nextSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#nextModal').modal('hide');
      var status = 3 // status++
      submit_interview_by_id(interview_id, "/api/interviews/", status, table);
    });
  });

  $(function() {
    $('#interviewFormSubmit2').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#interviewModal2').modal('hide');
      var status = 4 // status++
      submit_interview_by_id(interview_id, "/api/interviews/", status, table);
    });
  });


  $(function(){
    $('#interviewFormSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#interviewModal').modal('hide');
      var status = 3;

      submit_interview_by_id(interview_id, "/api/interviews/", status, table);
    });
  });

  $(function(){
    $('#offerFormSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#offerModal').modal('hide');
      var status = 4;

      submit_interview_by_id(interview_id, "/api/interviews/", status, table);
    });
  });

  $(function(){
    $('#entryFormSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#entryModal').modal('hide');
      var status = 5;

      submit_interview_by_id(interview_id, "/api/interviews/", status, table);
    });
  });

  $(function(){
    $('#inspectFormSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#inspectModal').modal('hide');
      var status = 6;

      submit_interview_by_id(interview_id, "/api/interviews/", status, table);
    });
  });

  $(function(){
    $('#paybackFormSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#paybackModal').modal('hide');
      var status = 7;

      submit_interview_by_id(interview_id, "/api/interviews/", status, table);
    });
  });

});
