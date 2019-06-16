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
  var post_selected = false;
  var post_selected_value = 0;

  var resumes_selected = [];
  var resume_selected_value = 0;

  var interview_selected_value = 0;

  var filter_status_value = 0;
  var enable_multi = false;

  function button_update(table, container, toggle_value) {
    if (!toggle_value) {
      list = container.classList;
      // Can't use toggleClass Here
      //node[0].toggleClass("btn-info");

      container.classList.remove("btn-info");
      container.innerText = "多选-关闭";

      //empty resumes
      resumes_selected = [];
      table.draw();
    } else {
      container.classList.add("btn-info");
      container.innerText = "多选-打开";
    }
  }

  var table = $('#dataTable_resume').DataTable({
    dom:
    "<'row'<'col-sm-12 col-md-1'l><'resume_multi col-sm-12 col-md-7'B><'col-sm-12 col-md-4'f>>" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
    buttons: [
      {text: '多选-关闭',
       action: function (e, dt, node, config) {
         enable_multi = !enable_multi;
         button_update(dt, node[0], enable_multi);
       }}
    ],
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
         if (filter_status_value == -1) {
           return `
                <div class="btn-group">
                --
                </div>
`;
         }
         else if (row.interview_status == 0) {
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
         // TBD: Do we need to restore resume_id into DOM data-resume_id in every element?
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

  /* ================================================================================ */

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
    } else if (enable_multi){
      // Multiple Selection
      var id = this.id;
      var index = $.inArray(id, resumes_selected);

      if ( index === -1 ) {
        resumes_selected.push(id);
      } else {
        resumes_selected.splice(index, 1);
      }

      $(this).toggleClass('selected');
    }
  });

  function page_refresh(table, reset_flag = false) {
    // update statistic info
    //var xx = t_resume_statistic_url;
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

    // TBD: We need a unified function for all initialization when switch different post.
    resumes_selected = [];
    enable_multi = false;

    // WTF? So many 0s... the first buttons's first child, there're two API:
    // containers() and container(), I can't distinguish them since both of them need to get [0]

    button_container = table.buttons().container()[0].children[0];
    button_update(table, button_container, enable_multi);

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

    xhr.onreadystatechange=function() {
      if (xhr.readyState === 4){   //if complete
        // 2xx is ok, ref: https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
        if(xhr.status >= 200 && xhr.status < 300) {
          //success
        } else {
          alert("Something error happend\n");
        }
      }
    }
    xhr.send(JSON.stringify(data));
  }

  function submit_interview_by_compound(resume_id, post_id, url, status_value, sub_status, is_active=true) {
    data = {"resume": resume_id,
            "post": post_id,
            "is_active": is_active,
            "status": status_value,
            "sub_status": sub_status,
            "result": is_active ? "Pending" : "Stopped",
           };

    xhr_common_send("POST", url, data);
  }

  // short-cut for xx-by_compound
  function submit_interview_by_id(interview_id, url, status_value, sub_status) {
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

  function helper_get_selectbox_text(select_id) {
    select_box = document.getElementById(select_id);
    text_box = select_box.options[select_box.selectedIndex].innerHTML;

    return text_box;
  }

  function helper_get_textbox_text(text_id) {
    text_box = document.getElementById(text_id);
    return text_box.value;
  }

  function show_post_modal(post_id, callback) {
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

        if (callback)
          $('#postModal').modal('toggle');
      },
      error: function() {
        console.log("get post info failed");
      },
    });
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

  function show_resume_modal(resume_id, callback) {
    $.ajax({
      url:'/api/resumes/' + resume_id + '/',
      type: 'GET',
      data: null,
      success: function(response) {

        document.getElementById("text_resumeinfo_username").value = response.username;
        document.getElementById("text_resumeinfo_degree").value = response.degree;
        document.getElementById("text_resumeinfo_school").value = response.school;
        document.getElementById("text_resumeinfo_phone_number").value = response.phone_number;

        if (callback)
          $('#resumeModal').modal('toggle');
      },
      error: function() {
        console.log("get resume info failed");
      },
    });
  }

  function show_callCandidate_modal(post_id, resume_id) {
    show_post_modal(post_id, false);
    show_resume_modal(resume_id, false);
    // TBD: no error handler
    $('#dailToCandidateModal').modal('toggle');
  }

  function show_entry_update_modal(interview_id) {
    $.ajax({
      url:'/interviews/sub/offer/' + interview_id + '/',
      type: 'GET',
      data: null,
      success: function(response) {

        document.getElementById("text_entryupdate_date").value = response.date;
        document.getElementById("text_entryupdate_contact").value = response.contact;
        document.getElementById("text_entryupdate_contact_phone").value = response.contact_phone;
        document.getElementById("text_entryupdate_address").value = response.address;
        document.getElementById("text_entryupdate_postname").value = response.postname;
        document.getElementById("text_entryupdate_certification").value = response.certification;
        document.getElementById("text_entryupdate_salary").value = response.salary;
        document.getElementById("text_entryupdate_notes").value = response.notes;

        $('#entryUpdateModal').modal('toggle');
      },
      error: function() {
        console.log("get sub offer info failed");
      },
    });
  }

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
    var statusI = 2;
    submit_interview_by_compound(resume_selected_value, post_selected_value, "/api/interviews/", statusI, '邀约')
  });

  $(document).on('click', '.stage_zero_fail', function() {
    resume_selected_value = Number(this.id);
    var statusI = 0;
    submit_interview_by_compound(resume_selected_value, post_selected_value, "/api/interviews/", statusI, "初选-终止", false)
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
    show_entry_update_modal(interview_selected_value);
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

  /* TBD: is this useful? */
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
      submit_interview_by_compound(resume_id, post_id, "/api/interviews/", status, 'AI面试');
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
      submit_interview_by_compound(resume_id, post_id, "/api/interviews/", status, 'AI面试');
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

        "expected_salary": helper_get_textbox_text("text_terminate_expected_salary"),
        "expected_notes": helper_get_textbox_text("text_terminate_expected_notes"),
        "expected_province": helper_get_textbox_text("text_terminate_expected_province"),
        "expected_city": helper_get_textbox_text("text_terminate_expected_city"),
        "expected_district": helper_get_textbox_text("text_terminate_expected_district"),

        "expected_insurance": helper_get_selectbox_text("text_terminate_expected_insurance"),
        "expected_insurance_schedule": helper_get_selectbox_text("text_terminate_expected_insurance_schedule")
      };

      submit_interviewsub_by_id("/interviews/api/terminate_sub/", table, data);
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
      submit_interview_by_id(interview_id, "/api/interviews/", status, '邀约');
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
        "comments": helper_get_textbox_text("text_interviewresult_comments"),
      };

      /* submit sub_interview_process_table, then the interview table is updated
         at the same time in the serverside */
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
        "date": helper_get_textbox_text("text_offerinfo_date"),
        "contact": helper_get_textbox_text("text_offerinfo_contact"),
        "contact_phone": helper_get_textbox_text("text_offerinfo_contact_phone"),
        "address": helper_get_textbox_text("text_offerinfo_address"),
        "postname": helper_get_textbox_text("text_offerinfo_postname"),
        "certification": helper_get_textbox_text("text_offerinfo_certification"),
        "salary": helper_get_textbox_text("text_offerinfo_salary"),
        "notes": helper_get_textbox_text("text_offerinfo_notes")

      };

      submit_interviewsub_by_id("/interviews/api/offer_sub_agree/", table, data);
    });
  });

  $(function(){
    $('#entryedSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#entryedModal').modal('hide');
      var status = 6;

      submit_interview_by_id(interview_id, "/api/interviews/", status, '考察');
    });
  });

  $(function(){
    // only update the entry info
    $('#entryUpdateSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#entryUpdateModal').modal('hide');
      //var status = 5;

      data = {
        "offer_sub": {
          "interview": interview_id,
          "result_type": 4
        },
        "date": helper_get_textbox_text("text_entryupdate_date"),
        "contact": helper_get_textbox_text("text_entryupdate_contact"),
        "contact_phone": helper_get_textbox_text("text_entryupdate_contact_phone"),
        "address": helper_get_textbox_text("text_entryupdate_address"),
        "postname": helper_get_textbox_text("text_entryupdate_postname"),
        "certification": helper_get_textbox_text("text_entryupdate_certification"),
        "salary": helper_get_textbox_text("text_entryupdate_salary"),
        "notes": helper_get_textbox_text("text_entryupdate_notes")

      };

      submit_interviewsub_by_id("/interviews/api/offer_sub_agree/", table, data);
    });
  });

  $(function(){
    // only update the entry info
    $('#probationSuccSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#probationSuccModal').modal('hide');
      var status = 7;

      submit_interview_by_id(interview_id, "/api/interviews/", status, '回款');
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
        "probation_sub": {
          "interview": interview_id,
          "result_type": 3
        },
        "reason": helper_get_textbox_text("text_probation_reason"),
        "comments": helper_get_textbox_text("text_probation_comments")
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

      submit_interview_by_id(interview_id, "/api/interviews/", status, '回款');
    });
  });

  $(function(){
    // only update the entry info
    $('#pbBaddebtSubmit').click(function(e){
      e.preventDefault();

      var interview_id = interview_selected_value;

      $('#pbBaddebtModal').modal('hide');
      var status = 7;

      submit_interview_by_id(interview_id, "/api/interviews/", status, '坏账');
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
        "notes": helper_get_textbox_text("text_pbfinish_notes")
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

      submit_interview_by_id(interview_id, "/api/interviews/", status, '已经注册');
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
        //"date": "2018-05-23 09:00",
        "date": helper_get_textbox_text("text_appointment_date"),
        "contact": helper_get_textbox_text("text_appointment_contact"),
        "address": helper_get_textbox_text("text_appointment_address"),
        "postname": helper_get_textbox_text("text_appointment_postname"),
        "certification": helper_get_textbox_text("text_appointment_certification"),
        "attention": helper_get_textbox_text("text_appointment_attention"),
        "first_impression": helper_get_textbox_text("text_appointment_first_impression"),
        "notes": helper_get_textbox_text("text_appointment_notes"),
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
      submit_interview_by_id(interview_id, "/api/interviews/", status, '深度沟通');
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
      submit_interview_by_id(interview_id, "/api/interviews/", status, '未接通');
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
});
