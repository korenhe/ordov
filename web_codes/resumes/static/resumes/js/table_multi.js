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
        d.degree_id_min = $('#degree_id_min').val();
        d.degree_id_max = $('#degree_id_max').val();
        d.age_id_min = $('#age_id_min').val();
        d.age_id_max = $('#age_id_max').val();
        d.graduate_time_min = $('#graduate_time_start').val();
        d.graduate_time_max = $('#graduate_time_end').val();
        d.gender_id = $('#gender_id').val();
        d.province = $('#working_place_province').val();
        d.city = $('#working_place_city').val();
        d.district = $('#working_place_district').val();
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

    /* default column 0 to desc ordering, how link 0 with the column id?*/
    "order": [[0, "desc"]],
    "columns": [
      {"data": null,
       "visible": false,
       "checkboxes": {
       },
      },
      {"data": "interview_id", "visible": false},
      {"data": "candidate_id", "visible": false},
      {"data": "id",
       "width": "1%"}, // resume id
      {"data": "username",
       "width": "1%",
       render: function(data, type, row, meta) {
         //var url = t_resume_detail_url;
         if (post_selected)
           return `
<a class="nav-link" href="/manager/resumes/` + row.id + `">` + data + `</a>
`;
         else
           return `
<a class="nav-link disabled" href="/manager/resumes/` + row.id + `">` + data + `</a>
`;
       }
      },
      {"data": "gender",
       "width": "1%",
       render: function(data, type, row, meta) {
         if (data == "Male") {
           return "男"
         } else if (data == "Female"){
           return "女"
         } else {
           // For default
           return "--"
         }
       },
      },
      {"data": "age",
       "width": "1%"},
      {"data": "phone_number", "visible":false},
      {"data": "email", "visible": false},
      {"data": "school",
       "width": "5%"},
      {"data": "degree",
       "width": "5%"},
      {"data": "major",
       "width": "5%"},

      {"data": "workexp",
       "orderable": false,
       "width": "20%"},
      {"data": "interview_status_name",
       "orderable": false,
       "width": "5%"
      },

      /* ================================================================================ */
      {"data": "interview_status",
       "orderable": false,
       "width": "15%",
       render: function(data, type, row, meta) {

         /* -------------------------------------------------------------------------------- */
         if (row.interview_status == 0) {
           return `
                <button class="invite_button btn btn-success border-0" id="` + row.id + `" style="display:none;">
                <span class="text">合适</span>
                </button>
                <button class="invite_button btn btn-success border-0" id="` + row.id + `" style="display:none;">
                <span class="text">操作</span>
                </button>

				<div class="btn-group">
                <select class="stage_zero_select form-control" id="` + row.id + `" style="display:none;">
                    <option>操作</option>
                    <option>AI沟通</option>
                    <option>短信沟通</option>
                </select>
				<button type="button" class="stage_zero_ai btn btn-sm " id="` + row.id + `">AI</button>
				<button type="button" class="stage_zero_sms btn btn-sm " id="` + row.id + `">短信</button>
				<button type="button" class="stage_zero_pass btn btn-sm " id="` + row.id + `">通过</button>
				<button type="button" class="stage_zero_fail btn btn-sm " id="` + row.id + `">结束</button>
				</div>

                <select class="stage_zero_select form-control" id="` + row.id + `" style="display:none;">
                    <option>待选状态</option>
                    <option>AI沟通</option>
                    <option>短信沟通</option>
                    <option>简历匹配</option>
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
                <select class="stage_one_select form-control" id="` + row.interview_id + `" style="display:none;">
                    <option>等待AI结果</option>
                    <option>继续下轮过程</option>
                    <option>终止面试</option>
                </select>

				<div class="btn-group">
                <select class="stage_one_select form-control" id="` + row.interview_id + `" style='display:none;'>
                    <option>操作</option>
                </select>
				<button type="button" class="stage_one_pass btn btn-sm " id="` + row.interview_id + `">通过</button>
				<button type="button" class="stage_one_fail btn btn-sm " id="` + row.interview_id + `">结束</button>
				</div>

`;
         }
         /* -------------------------------------------------------------------------------- */
         else if (row.interview_status == 2) {
           return `
				<div class="btn-group">
                <select class="stage_two_select form-control" id="` + row.interview_id + `" data-resume_id="` + row.id + `" style="display:none;">
                    <option>拨号面试</option>
                    <option>深度沟通</option>
                    <option>电话未接通</option>
                </select>
				<button type="button" class="stage_two_dail btn btn-sm " id="` + row.interview_id + `" data-resume_id="` + row.id + `">拨号面试</button>
				<button type="button" class="stage_two_pass btn btn-sm " id="` + row.interview_id + `" data-resume_id="` + row.id + `">通过</button>
				<button type="button" class="stage_two_fail btn btn-sm " id="` + row.interview_id + `" data-resume_id="` + row.id + `">结束</button>
				</div>

`;
         }
         /* -------------------------------------------------------------------------------- */
         else if (row.interview_status == 3) {
           return `
				<div class="btn-group">
                <select class="stage_three_select form-control" id="` + row.interview_id + `" data-resume_id="` + row.id + `" style="display:none;">
                    <option>操作</option>
                    <option>面试未到场</option>
                </select>
				<button type="button" class="stage_three_miss btn btn-sm " id="` + row.interview_id + `" data-resume_id="` + row.id + `">未到场</button>
				<button type="button" class="stage_three_pass btn btn-sm " id="` + row.interview_id + `" data-resume_id="` + row.id + `">通过</button>
				<button type="button" class="stage_three_fail btn btn-sm " id="` + row.interview_id + `" data-resume_id="` + row.id + `">未通过</button>
				</div>
`;
         }
         /* -------------------------------------------------------------------------------- */
         else if (row.interview_status == 4) {
           return `
				<div class="btn-group">
                <select class="stage_four_select form-control" id="` + row.interview_id + `" data-resume_id="` + row.id + `" style="display:none;">
                    <option>操作</option>
                    <option>更新offer</option>
                </select>
				<button type="button" class="stage_four_update btn btn-sm " id="` + row.interview_id + `" data-resume_id="` + row.id + `">更新</button>
				<button type="button" class="stage_four_pass btn btn-sm " id="` + row.interview_id + `" data-resume_id="` + row.id + `">接受</button>
				<button type="button" class="stage_four_fail btn btn-sm " id="` + row.interview_id + `" data-resume_id="` + row.id + `">放弃</button>
				</div>
`;
         }
         /* -------------------------------------------------------------------------------- */
         else if (row.interview_status == 5) {
           return `
				<div class="btn-group">
                <select class="stage_five_select form-control" id="` + row.interview_id + `" data-resume_id="` + row.id + `" style="display:none;">
                    <option>操作</option>
                    <option>更期入职</option>
                </select>
				<button type="button" class="stage_five_update btn btn-sm " id="` + row.interview_id + `" data-resume_id="` + row.id + `">更期入职</button>
				<button type="button" class="stage_five_pass btn btn-sm " id="` + row.interview_id + `" data-resume_id="` + row.id + `">已入职</button>
				<button type="button" class="stage_five_fail btn btn-sm " id="` + row.interview_id + `" data-resume_id="` + row.id + `">放弃</button>
				</div>
`;
         }
         /* -------------------------------------------------------------------------------- */
         else if (row.interview_status == 6) {
           return `
				<div class="btn-group">
                <select class="stage_six_select form-control" id="` + row.interview_id + `" data-resume_id="` + row.id + `" style="display:none;">
                    <option>操作</option>
                    <option>放弃考察</option>
                </select>
				<button type="button" class="stage_six_giveup btn btn-sm " id="` + row.interview_id + `" data-resume_id="` + row.id + `">放弃考察</button>
				<button type="button" class="stage_six_pass btn btn-sm " id="` + row.interview_id + `" + data-resume_id="` + row.id + `">通过</button>
				<button type="button" class="stage_six_fail btn btn-sm " id="` + row.interview_id + `" + data-resume_id="` + row.id + `">未通过</button>
				</div>

`;
         }
         /* -------------------------------------------------------------------------------- */
         else if (row.interview_status == 7) {
           return `
				<div class="btn-group">
				<button type="button" class="stage_seven_register btn btn-sm " id="` + row.interview_id + `" data-resume_id="` + row.id + `">登记</button>
				<button type="button" class="stage_seven_bill btn btn-sm " id="` + row.interview_id + `" data-resume_id="` + row.id + `">发票</button>
				<button type="button" class="stage_seven_pass btn btn-sm " id="` + row.interview_id + `" data-resume_id="` + row.id + `">完成</button>
				<button type="button" class="stage_seven_fail btn btn-sm " id="` + row.interview_id + `" data-resume_id="` + row.id + `">坏账</button>
				</div>
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
    "dom": '<"top"i>rt<"bottom"l<"post_search" f>p><"clear">',
    "lengthChange": false,
    "pageLength" : 15,
    "pagingType": "simple",
    "processing": false,
    "serverSide": true,

    "scrollX": false,
    "scrollCollapse": false,
    "searching": true,

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
      {"data": "project_name",
      },
    ],
  });

  /* ======================================== Process Begin Here */

  $('#age_id_min, #age_id_max').keyup(function() {
    page_refresh(table, true);
  });

  $('#working_place_province, #working_place_city, #working_place_district').keyup(function() {
    page_refresh(table, true);
  });

  $('.list-group-item').on('click', function(e) {
    filter_status_value = this.value;
    page_refresh(table, true);
  });

  $('#degree_id_min, #gender_id, #degree_id_max').change(function() {
    page_refresh(table, true);
  });

  $('#graduate_time_start, #graduate_time_end').change(function() {
    page_refresh(table, true);
  });

  // resume table
  $('#dataTable_resume tbody').on('click', 'tr', function(e) {
    if (post_selected == false) {
      //alert("Please select Post first.");
      alert("请先选择职位.");
      e.stopPropagation();
    } else {
    }
  });

  function page_refresh(table, reset_flag = false) {
    // update statistic info
    var xx = t_resume_statistic_url;
    $.ajax({
      url: "/manager/resumes/statistic/" + post_selected_value + "/",
      type: 'GET',
      data: null,
      success: function(response) {
        document.getElementById("badge_statistic_stage_0").innerHTML = response.resumes_waitting;
        for (var i = 1; i < 10; i++) {
          document.getElementById("badge_statistic_stage_" + i).innerHTML = response.interviews_status_filters[i-1];
        }
      },
      error: function() {
        console.log("get statistic info failed");
      },
    });

    table.draw(reset_flag);
  }

  function xhr_common_send(method, url, data) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url);

    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    var csrftoken = getCookie('csrftoken');

    xhr.setRequestHeader("X-CSRFToken", csrftoken);

    xhr.onloadend = function() {
      //done
      page_refresh(table);
    };

    xhr.send(JSON.stringify(data));
  }

  function stop_interview_by_compound(resume_id, post_id, url, status_value, table) {
    data = {"resume": resume_id,
            "post": post_id,
            "is_active":false,
            "status": status_value,
            "sub_status": "初选-终止",
            "result":"Stopped",
           };
    xhr_common_send("POST", url, data);
  }

  function submit_interview_by_compound(resume_id, post_id, url, status_value, sub_status, table) {
    data = {"resume": resume_id,
            "post": post_id,
            "is_active":true,
            "status": status_value,
            "sub_status": sub_status,
            "result":"Pending",
           };

    xhr_common_send("POST", url, data);
  }

  function submit_interview_by_id(interview_id, url, status_value, sub_status, table) {
    data = {"is_active":true,
            "status": status_value,
            "result":"Pending",
            "sub_status":sub_status,
           };

    xhr_common_send("PATCH", url + interview_id + '/', data);
  }

  /* Save Interview Sub Table */
  function submit_interviewsub_by_id(url, table, data) {
    xhr_common_send("POST", url, data);
  }

  function terminate_interviewsub_by_id(url, table, data) {
    xhr_common_send("POST", url, data);
  }

  function helper_get_selectbox_text(select_id) {
    select_box = document.getElementById(select_id);
    text_box = select_box.options[select_box.selectedIndex].innerHTML;

    return text_box;
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


  function show_callCandidate_modal(post_id, resume_id) {
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
      },
      error: function() {
        console.log("get post info failed");
      },
    });

    $.ajax({
      url:'/api/resumes/' + resume_id + '/',
      type: 'GET',
      data: null,
      success: function(response) {

        document.getElementById("candidate_text_resumeinfo_username").value = response.username;
        document.getElementById("candidate_text_resumeinfo_degree").value = response.degree;
        document.getElementById("candidate_text_resumeinfo_school").value = response.school;
        document.getElementById("candidate_text_resumeinfo_phone_number").value = response.phone_number;

      },
      error: function() {
        console.log("get resume info failed");
      },
    });
    $('#dailToCandidateModal').modal('toggle');
  }


  function show_ai_config_modal(resume_id) {
    $.ajax({
      url:'/api/resumes/' + resume_id + '/',
      type: 'GET',
      data: null,
      success: function(response) {

        document.getElementById("text_name").value = response.username;
        document.getElementById("text_phone_number").value = response.phone_number;

        $('#dialModal').modal('toggle');
      },
      error: function() {
        console.log("get resume info failed");
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

  $(document).on('click', '.stage_zero_ai', function() {
	resume_selected_value = Number(this.id);
    show_ai_config_modal(resume_selected_value)
  });

  $(document).on('click', '.stage_zero_sms', function() {
  });

  $(document).on('click', '.stage_zero_pass', function() {
    resume_selected_value = Number(this.id);
    var statusI = 2
    submit_interview_by_compound(resume_selected_value, post_selected_value, "/api/interviews/", statusI, '邀约', table)

  });

  $(document).on('click', '.stage_zero_fail', function() {
    resume_selected_value = Number(this.id);
    var statusI = 0
    stop_interview_by_compound(resume_selected_value, post_selected_value, "/api/interviews/", statusI, table)
  });

  $(document).on('click', '.stage_one_pass', function() {
    interview_selected_value = Number(this.id);
    $('#nextModal').modal('toggle')
  });
  $(document).on('click', '.stage_one_fail', function() {
    interview_selected_value = Number(this.id);
    $('#stopModal').modal('toggle')
  });

  $(document).on('click', '.stage_two_dail', function() {
    interview_selected_value = Number(this.id);
    resume_id = this.dataset.resume_id;
    show_callCandidate_modal(post_selected_value, resume_id)
  });
  $(document).on('click', '.stage_two_pass', function() {
    interview_selected_value = Number(this.id);
    $('#appointmentModal').modal('toggle')
  });
  $(document).on('click', '.stage_two_fail', function() {
    interview_selected_value = Number(this.id);
    $('#stopModal').modal('toggle')
  });

  $(document).on('click', '.stage_three_miss', function() {
    interview_selected_value = Number(this.id);
    $('#stopModal').modal('toggle');
  });
  $(document).on('click', '.stage_three_pass', function() {
    interview_selected_value = Number(this.id);
    $('#interviewResultModal').modal('toggle')
  });
  $(document).on('click', '.stage_three_fail', function() {
    interview_selected_value = Number(this.id);
    $('#stopModal').modal('toggle')
  });

  $(document).on('click', '.stage_four_update', function() {
    interview_selected_value = Number(this.id);
    $('#offerModal').modal('toggle')
  });
  $(document).on('click', '.stage_four_pass', function() {
    interview_selected_value = Number(this.id);
    $('#offerModal').modal('toggle')
  });
  $(document).on('click', '.stage_four_fail', function() {
    interview_selected_value = Number(this.id);
    $('#stopModal').modal('toggle')
  });

  $(document).on('click', '.stage_five_update', function() {
    interview_selected_value = Number(this.id);
    $('#entryUpdateModal').modal('toggle');
  });
  $(document).on('click', '.stage_five_pass', function() {
    interview_selected_value = Number(this.id);
    $('#entryedModal').modal('toggle')
  });
  $(document).on('click', '.stage_five_fail', function() {
    interview_selected_value = Number(this.id);
    $('#stopModal').modal('toggle')
  });

  $(document).on('click', '.stage_six_giveup', function() {
    interview_selected_value = Number(this.id);
    $('#stopModal').modal('toggle');
  });
  $(document).on('click', '.stage_six_pass', function() {
    interview_selected_value = Number(this.id);
    $('#probationSuccModal').modal('toggle')
  });
  $(document).on('click', '.stage_six_fail', function() {
    interview_selected_value = Number(this.id);
    $('#probationFailModal').modal('toggle')
  });


  $(document).on('click', '.stage_seven_register', function() {
    interview_selected_value = Number(this.id);
    $('#pbRegisterModal').modal('toggle')
  });
  $(document).on('click', '.stage_seven_bill', function() {
    interview_selected_value = Number(this.id);
    $('#pbInvoiceModal').modal('toggle')
  });
  $(document).on('click', '.stage_seven_pass', function() {
    interview_selected_value = Number(this.id);
    $('#pbFinishModal').modal('toggle')
  });
  $(document).on('click', '.stage_seven_fail', function() {
    interview_selected_value = Number(this.id);
    $('#pbBaddebtModal').modal('toggle');
    //$('#stopModal').modal('toggle')
  });

  // use 'click' here, otherwise, if user select 'next' and then closed, he should change to other stats then back to 'next' to trigger the event.
  $(document).on('click', '.stage_zero_select', function() {
	resume_selected_value = Number(this.id);

    /* Attention: how to select one item by variable */
    /*value = $(".stage_zero_select:eq("+(resume_selected_value-1)+")").val() */
    /* the intersection selector for jQuery */

    value = $("#"+(resume_selected_value)+".stage_zero_select").val()
    if (value == "AI沟通") {
       show_ai_config_modal(resume_selected_value)
    } else if (value == "短信沟通") {
    } else if (value == "简历匹配") {
       $('#nextModal').modal('toggle')
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

  $(document).on('change', '.stage_two_select', function() {
    interview_selected_value = Number(this.id);
    value = $("#"+(interview_selected_value)+".stage_two_select").val()
    if (value == "自动拨号") {
    } else if (value == "拨号面试") {
      resume_id = this.dataset.resume_id;
      show_callCandidate_modal(post_selected_value, resume_id)
    } else if (value == "应聘者信息") {
      $('#resumeModal').modal('toggle');
      resume_id = this.dataset.resume_id;
      show_resume_modal(resume_id);
    } else if (value == "同意面试") {
      $('#appointmentModal').modal('toggle');
    } else if (value == "放弃面试") {
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
    } else if (value == "面试通过") {
      $('#interviewResultModal').modal('toggle');
    } else if (value == "面试未通过") {
      $('#stopModal').modal('toggle');
    } else if (value == "面试未到场") {
      $('#stopModal').modal('toggle');
    }
  });

  $(document).on('click', '.stage_four_select', function() {
    interview_selected_value = Number(this.id);

    value = $("#"+(interview_selected_value)+".stage_four_select").val()
    if (value == "发放offer") {
    } else if (value == "更新offer") {
      $('#offerModal').modal('toggle')
    } else if (value == "放弃offer") {
      $('#stopModal').modal('toggle');
    }
  });

  $(document).on('click', '.stage_five_select', function() {
    interview_selected_value = Number(this.id);

    value = $("#"+(interview_selected_value)+".stage_five_select").val()
    if (value == "入职过程") {
    } else if (value == "入职到场") {
      $('#entryedModal').modal('toggle')
    } else if (value == "放弃入职") {
      $('#stopModal').modal('toggle')
    } else if (value == "更期入职") {
      $('#entryUpdateModal').modal('toggle');
    }
  });

  $(document).on('click', '.stage_six_select', function() {
    interview_selected_value = Number(this.id);

    value = $("#"+(interview_selected_value)+".stage_six_select").val()
    if (value == "考察期") {
    } else if (value == "通过考察") {
      $('#probationSuccModal').modal('toggle')
    } else if (value == "未通过考察") {
      $('#probationFailModal').modal('toggle')
    } else if (value == "放弃考察") {
      $('#stopModal').modal('toggle');
    }
  });

  $(document).on('click', '.stage_seven_select', function() {
    interview_selected_value = Number(this.id);

    value = $("#"+(interview_selected_value)+".stage_seven_select").val()
    if (value == "回款阶段") {
    } else if (value == "打款登记") {
      $('#pbRegisterModal').modal('toggle')
    } else if (value == "完成打款") {
      $('#pbFinishModal').modal('toggle')
    } else if (value == "坏账") {
      $('#pbBaddebtModal').modal('toggle');
    } else if (value == "发票申请") {
      $('#pbInvoiceModal').modal('toggle');
    }
  });

  $(document).on('change', '#ai_task_id', function() {
      var condition = $("#ai_task_id").find("option:selected").text()
      // should update the huashu ID corresponsely
  });

  // post table
  $('#dataTable_post tbody').on('click', 'tr', function() {
    var id = this.id;

    if (id === post_selected_value && post_selected === true) {
      $(this).toggleClass('selected');
      post_selected = false;

      document.getElementById("text_company_name").innerHTML = "选择项目";
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

  $(function(){
    $('#inviteFormSubmit').click(function(e){
      e.preventDefault();
      var resume_id = resume_selected_value;
      var post_id = post_selected_value;
      var status = 1;

      alert("Resume:" + resume_id + " :Post:" + post_id);
      $('#inviteModal').modal('hide');
      //$('#formResults').text($('#myForm').serialize());
      submit_interview_by_compound(resume_id, post_id, "/api/interviews/", status, 'AI面试', table);
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
      submit_interview_by_compound(resume_id, post_id, "/api/interviews/", status, 'AI面试', table);
    });
  });

  $(function() {
    $('#stopFormSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#stopModal').modal('hide');

      data = {
        "interview": interview_id,
        "expected_industry": helper_get_selectbox_text("text_terminate_expected_industry"),
        "expected_post": helper_get_selectbox_text("text_terminate_expected_post"),
        "expected_shift": helper_get_selectbox_text("text_terminate_expected_shift"),
        "expected_salary": "t sa",
        "expected_notes": "t n",
        "expected_province": "t p",
        "expected_city": "t c",
        "expected_district": "t d",
        "expected_insurance": "t in",
        "expected_insurance_schedule": "t ins"
      };

      terminate_interviewsub_by_id("/interviews/api/terminate_sub/", table, data);
    });
  });

  $(function() {
    $('#nextSubmit').click(function(e){
      e.preventDefault();
      var resume_id = resume_selected_value;
      var post_id = post_selected_value;
      var interview_id = interview_selected_value;
      var status = 2;

      $('#nextModal').modal('hide');
      //submit_interview_by_compound(resume_id, post_id, "/api/interviews/", status, table);
      submit_interview_by_id(interview_id, "/api/interviews/", status, '邀约', table);
    });
  });

  $(function() {
    $('#interviewResultFormSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#interviewResultModal').modal('hide');
      //var status = 4;

      data = {
        "interview_sub": {
          "interview": interview_id,
          "result_type": 3
        },
        "reason": "interview pass reason",
        "description": "interview pass description",
        "comments": "interview pass comments",
        "notes": "interview pass notes"
      };

      /* submit sub_interview_process_table, then the interview table is updated
         at the same time in the serverside */
      //submit_interview_by_id(interview_id, "/api/interviews/", status, table);
      submit_interviewsub_by_id("/interviews/api/interview_sub_pass/", table, data);
    });
  });

  $(function(){
    $('#offerSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#offerModal').modal('hide');
      //var status = 5;

      data = {
        "offer_sub": {
          "interview": interview_id,
          "result_type": 3
        },
        "date": null,
        "contact": "offer agree c",
        "contact_phone": "offer agree cp",
        "address": "offer agree add",
        "postname": "offer agree p",
        "certification": "offer agree cert",
        "salary": "offer agree salary",
        "notes": "offer agree notes"
      };

      //submit_interview_by_id(interview_id, "/api/interviews/", status, table);
      submit_interviewsub_by_id("/interviews/api/offer_sub_agree/", table, data);
    });
  });

  $(function(){
    $('#entryedSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#entryedModal').modal('hide');
      var status = 6;

      submit_interview_by_id(interview_id, "/api/interviews/", status, '考察', table);
    });
  });

  $(function(){
    // only update the entry info
    $('#entryUpdateSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#entryUpdateModal').modal('hide');
      var status = 5;

      submit_interview_by_id(interview_id, "/api/interviews/", status, '入职', table);
    });
  });

  $(function(){
    // only update the entry info
    $('#probationSuccSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#probationSuccModal').modal('hide');
      var status = 7;

      submit_interview_by_id(interview_id, "/api/interviews/", status, '回款', table);
    });
  });

  $(function(){
    // only update the entry info
    $('#probationFailSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#probationFailModal').modal('hide');
      // active = false
      data = {
        "payback_sub": {
        "interview": interview_id,
        "result_type": 3
        },

        "reason": "pb failed reason",
        "comments": "pb failed comments"
      };

      /* This is different with other terminate modal, because it contains the probation fail reason */
      submit_interviewsub_by_id("/interviews/api/probation_sub_fail/", table, data);
    });
  });

  $(function(){
    // only update the entry info
    $('#pbInvoiceSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#pbInvoiceModal').modal('hide');
      var status = 7;

      submit_interview_by_id(interview_id, "/api/interviews/", status, '回款', table);
    });
  });

  $(function(){
    // only update the entry info
    $('#pbBaddebtSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#pbBaddebtModal').modal('hide');
      var status = 7;

      submit_interview_by_id(interview_id, "/api/interviews/", status, '坏账', table);
    });
  });

  $(function(){
    // only update the entry info
    $('#pbFinishSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#pbFinishModal').modal('hide');

      // status = 8
      data = {
        "payback_sub": {
        "interview": interview_id,
        "result_type": 3
        },
        "notes": "payback notes"
      };

      submit_interviewsub_by_id("/interviews/api/payback_sub_finish/", table, data);
    });
  });

  $(function(){
    // only update the entry info
    $('#pbRegisterSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#pbRegisterModal').modal('hide');
      var status = 7;

      submit_interview_by_id(interview_id, "/api/interviews/", status, '已经注册', table);
    });
  });
  //------------------------------------------Current

  $(function() {
    $('#appointmentSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#appointmentModal').modal('hide');
      //var status = 3 // interview

      data = {
        "appointment_sub": {
          "interview": interview_id,
          "result_type": 3
        },
        "date": null,
        "contact": "app agree c",
        "address": "app agree a",
        "postname": "app agree p",
        "certification": "app agree cert",
        "attention": "app agree att",
        "first_impression": "app agree fi",
        "notes": "app agree notes"
      };

      submit_interviewsub_by_id("/interviews/api/appointment_sub_agree/", table, data);
    });
  });

  $(function() {
    $('#agree_interview').click(function(e){
        $('#dailToCandidateModal').modal('hide');
        $('#appointmentModal').modal('show');
    });
  });

  $(function() {
    $('#dail_deeper_communicate').click(function(e){
      e.preventDefault();
      var resume_id = resume_selected_value;
      var post_id = post_selected_value;
      var interview_id = interview_selected_value;
      var status = 2;
      $('#dailToCandidateModal').modal('hide');
      //submit_interview_by_compound(resume_id, post_id, "/api/interviews/", status, table);
      submit_interview_by_id(interview_id, "/api/interviews/", status, '深度沟通', table);
    });
  });

  $(function() {
    $('#dail_not_linked').click(function(e){
      e.preventDefault();
      var resume_id = resume_selected_value;
      var post_id = post_selected_value;
      var interview_id = interview_selected_value;
      var status = 2;
      $('#dailToCandidateModal').modal('hide');
      //submit_interview_by_compound(resume_id, post_id, "/api/interviews/", status, table);
      submit_interview_by_id(interview_id, "/api/interviews/", status, '未接通', table);
    });
  });

  $(function() {
    $('#giveup_interview').click(function(e){
        $('#dailToCandidateModal').modal('hide');
        $('#stopModal').modal('show');
    });
  });

  //-------- select
    $.ajax({
      type: "GET",
      url:'/interview/ai/task',
      async:false,
      dataType: "json",
      success: function(data){
        $('#ai_task_id').html("")
        $('#ai_task_id').prepend('<option value="">请选择任务</option>');
        if (data !='') {
          $.each(data.ai_taskId,function(index, ele) {
            $('#ai_task_id').append('<option value="ai_task_id' + index + '">' + ele + '</option>');
          });
        }
      }
    });
   //-----------
   //------------modal
   //-----------
});
