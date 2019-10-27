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

  var interviews_selected = [];
  var interview_selected_value = 0;

  var filter_status_value = 0;
  var enable_multi = false;

  function empty_multi_selection() {
    //empty resumes
    resumes_selected = [];
    interviews_selected = [];
  }

  /* return redrawed */
  function button_update(table, container, toggle_value) {
    if (!toggle_value) {
      list = container.classList;
      // Can't use toggleClass Here
      //node[0].toggleClass("btn-info");

      container.classList.remove("btn-info");
      container.innerText = "多选[N]";

      empty_multi_selection();
      table.draw();
      return true;
    } else {
      container.classList.add("btn-info");
      container.innerText = "多选[Y]";
      return false;
    }
  }

  var table = $('#dataTable_resume').DataTable({
    dom:
    "<'row'      <'col-sm-12 col-md-8'<'row' <'resume_multi ml-3'B><'ml-3'l>>>       <'col-sm-12 col-md-4'f>   >" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
    buttons: [
      {text: '多选[N]',
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
      {"data": "newname",
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
      {"data": "expected",
       "width": "5%"
      },
      {"data": "ageg",
       "width": "5%"
      },
      {"data": "phone_number", "visible":false},
      {"data": "email", "visible": false},
      {"data": "majorfull",
       "width": "10%"},

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
                <div class="btn-group">
                <button type="button" class="stage_zero_ai btn btn-sm " id="` + row.id + `">AI</button>
                <button type="button" class="stage_zero_sms btn btn-sm " id="` + row.id + `">短信</button>
                <button type="button" class="stage_zero_pass btn btn-sm " id="` + row.id + `">通过</button>
                <button type="button" class="stage_zero_fail btn btn-sm " id="` + row.id + `">结束</button>
                </div>
          `;
         }
         /* -------------------------------------------------------------------------------- */
         else if (row.interview_status == 1) {
           return `
                <div class="btn-group">
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

  $(function(){
    /* flush table every 100s */
    setInterval(flush,100000);
    function flush(){
        if (post_selected_value > 0) {
            page_refresh(table, true);
        }
    }
  })

  $('#age_id_min, #age_id_max').keyup(function() {
    page_refresh(table, true);
  });

  $('#working_place_province, #working_place_city, #working_place_district').keyup(function() {
    page_refresh(table, true);
  });

  $('#degree_id_min, #gender_id, #degree_id_max').change(function() {
    page_refresh(table, true);
  });

  $('#graduate_time_start, #graduate_time_end').change(function() {
    page_refresh(table, true);
  });

  $('#closeProject').click(function() {
    $('#projectPanel').css('display', 'none')
    $('#mainOpPanel').removeClass('col-md-10')
    $('#mainOpPanel').addClass('col-md-12')
    // show the right arrow in the left side
    $('#projectSelectShow').css('display', 'inline')
  });

  $('#projectSelectShow').click(function() {
    $('#projectPanel').css('display', 'inline')
    $('#mainOpPanel').removeClass('col-md-12')
    $('#mainOpPanel').addClass('col-md-10')
    // show the right arrow in the left side
    $('#projectSelectShow').css('display','none')
  });

  $('.list-group-item').on('click', function(e) {
    filter_status_value = this.value;
    page_refresh(table, true);
  });

  $('#table_Status').on('click', function(e) {
    if (post_selected == false) {
      alert("请先选择职位.");
      e.stopPropagation();
    } else {
      $('#ai_status').val('-')
      $('#ai_status_action').val('-')
      $('#ai_status_and_action').val('-')
      $('#aiSelectModal').modal('toggle')
    }
  });

  $('#ai_status_action').on('change', function(e) {
    var newStr = "对于AI状态: "+$('#ai_status').val() +" 的记录,"+ "作"+$('#ai_status_action').val()+"处理"
    console.log(newStr)
    $('#ai_status_and_action').val(newStr)
  });

  $('#aiStatusActionSubmit').on('click', function(e) {
    var post_id = post_selected_value
    $.ajax({
      method: "POST",
      url: "/interview/ai/update/",
      data: {
        post_id: post_id,
        ai_status: $('#ai_status').val(),
        ai_status_action: $('#ai_status_action').val(),
      },
      success: function(response) {
        page_refresh(table, true);
        $('#ai_status').val('-')
        $('#ai_status_action').val('-')
        $('#ai_status_and_action').val('done!')
      },
    });
  });

  function format(d) {
    var data = format_inner(d)
    var sData = JSON.parse(data)
    return '<div class=".container">'+
        '<div class="row">'+
          '<div class="col-md-2">'+
          '</div>' +
          '<div class="col-md-2">'+
            '<p style="display:inline;">'+"籍贯:"+'</p>'+
            '<p style="display:inline;">'+sData.birthorigin+'</p>'+
          '</div>' +
          '<div class="col-md-2">'+
            '<p style="display:inline;">'+"电话:"+'</p>'+
            '<p style="display:inline;">'+sData.phone_number+'</p>'+
          '</div>' +
          '<div class="col-md-4">'+
            '<p style="display:inline;">'+"毕业时间:"+'</p>'+
            '<p style="display:inline;">'+sData.graduate_time+'</p>'+
          '</div>' +
        '</div>'+
        '<div class="row">'+
          '<div class="col-md-2">'+
          '</div>' +
          '<div class="col-md-2">'+
          '</div>' +
          '<div class="col-md-8">'+
          '</div>'+
        '</div>'+
        '<div class="row">'+
          '<div class="col-md-2">'+
          '</div>' +
          '<div class="col-md-2">'+
            '<span>'+ "现工作地:" +'</span>'+
          '</div>' +
          '<div class="col-md-8">'+
            '<span>' + "--" + '</span>'+
          '</div>'+
        '</div>'+
        '<div class="row">'+
          '<div class="col-md-2">'+
          '</div>' +
          '<div class="col-md-2">'+
            '<span>'+ "期望工作地点:" +'</span>'+
          '</div>' +
          '<div class="col-md-8">'+
            '<span>' + sData.expected + '</span>'+
          '</div>'+
        '</div>'+
        '<div class="row">'+
          '<div class="col-md-2">'+
          '</div>' +
          '<div class="col-md-2">'+
            '<span>'+ "期望岗位类型:" +'</span>'+
          '</div>' +
          '<div class="col-md-8">'+
            '<span>' + "--" + '</span>'+
          '</div>'+
        '</div>'+
        '<div class="row">'+
          '<div class="col-md-2">'+
          '</div>' +
          '<div class="col-md-2">'+
            '<span>'+ "期望薪资:" +'</span>'+
          '</div>' +
          '<div class="col-md-8">'+
            '<span>' + "--" + '</span>'+
          '</div>'+
        '</div>'+
        '<div class="row">'+
          '<div class="col-md-2">'+
          '</div>' +
          '<div class="col-md-2">'+
            '<span>'+ "最近一份工作经历:" +'</span>'+
          '</div>' +
          '<div class="col-md-8">'+
            '<span>' + sData.workexp + '</span>'+
          '</div>'+
        '</div>'+
        '<div class="row">'+
          '<div class="col-md-2">'+
       '</div>' +
          '<div class="col-md-2">'+
            '<span>'+ "最高学历:" +'</span>'+
          '</div>' +
          '<div class="col-md-8">'+
            '<span>' + sData.school+ ' ' + sData.major + ' ' + sData.degree +'</span>'+
          '</div>'+
        '</div>'+
        '</div>';
  };

  function format_inner(d) {
	var resume_id = d.id
	return $.ajax({
	  url: '/api/resumes/' + resume_id + '/',
	  type: 'GET',
	  data: null,
	  async: false
	}).responseText;
  };

  // resume table
  $('#dataTable_resume tbody').on('click', 'tr', function(e) {
    if (post_selected == false) {
      //alert("Please select Post first.");
      alert("请先选择职位.");
      e.stopPropagation();
    } else {
      // All interactive elements should be excluded here.
      if ($(e.target).hasClass('btn')) {
        return;
      }

      if (enable_multi) {
        // Multiple Selection
        var id = this.id;
        var interview_id = -1;
        try {
          // TBD: more gerneric and accurate way to get interview_id
          interview_id = this.lastChild.firstElementChild.firstElementChild.id;
          if (interview_id === "")
            interview_id = -1;
        } catch {
          interview_id = -1;
        }

        var index = $.inArray(id, resumes_selected);

        if ( index === -1 ) {
          resumes_selected.push(id);

          if (interview_id >= 0)
            interviews_selected.push(interview_id);
        } else {
          resumes_selected.splice(index, 1);

          if (interview_id >= 0)
            interviews_selected.splice(index, 1);
        }

        $(this).toggleClass('selected');
      } else { // not enable_multi
		var tr = $(this).closest('tr')
		var row = table.row(tr)
		if (row.child.isShown()) {
		  row.child.hide();
		  tr.removeClass('shown')
		}
		else {
		  // Open this row
		  row.child(format(row.data())).show();
		  row.child(format(row.data())).show()
		  tr.addClass('shown')
        }
      }
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

    empty_multi_selection();
    enable_multi = false;

    // WTF? So many 0s... the first buttons's first child, there're two API:
    // containers() and container(), I can't distinguish them since both of them need to get [0]

    button_container = table.buttons().container()[0].children[0];
    redrawed = button_update(table, button_container, enable_multi);

    if (!redrawed)
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
          console.log("csrftoken: ", csrftoken)
		  console.log(xhr.responseText)
		  console.log(xhr.status)
		  console.log(xhr.statusText)
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

  /* Save Interview Sub Table */
  function submit_interviewsub_by_id_test(url, table, data) {
    xhr_common_send("GET", url, data);
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
      url:'/api/posts/' + post_selected_value + '/',
      type: 'GET',
      data: null,
      success: function(response) {
        document.getElementById("config_ai_task_name").value = response.baiying_task_name;
      },
      error: function() {
        console.log("get resume info failed");
      },
    });
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

        document.getElementById("candidate_text_resumeinfo_username").value = response.username;
        document.getElementById("candidate_text_resumeinfo_degree").value = response.degree;
        document.getElementById("candidate_text_resumeinfo_school").value = response.school;
        document.getElementById("candidate_text_resumeinfo_phone_number").value = response.phone_number;

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

  function show_stop_modal(interview_id, resume_id) {
    $.ajax({
      url:'/api/resumes/' + resume_id + '/',
      type: 'GET',
      data: null,
      success: function(response) {
        document.getElementById("text_terminate_expected_province").value = response.expected_province;
        document.getElementById("text_terminate_expected_city").value = response.expected_city;
        document.getElementById("text_terminate_expected_district").value = response.expected_district;
      },
      error: function() {
        console.log("get resume info failed");
      },
    });
    $('#stopModal').modal('toggle')
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

  // ================================= CLICKS ===============================================
  function tmp_not_support_multi() {
    if (enable_multi)
      alert("This button not support multi-sel event yet!");
  }

  function multisel_submit_wrapper(callback) {
    if (!enable_multi) {
      callback(interview_selected_value);
    } else {
      for (var i = 0; i < interviews_selected.length; i++) {
        callback(interviews_selected[i]);
      }
    }
  }

  function multisel_submit_wrapper_resumeid(callback) {
    if (!enable_multi) {
      callback(resume_selected_value);
    } else {
      for (var i = 0; i < resumes_selected.length; i++) {
        callback(resumes_selected[i]);
      }
    }
  }

  function do_common_plain_submit(interview_id, modal_name, status, sub_status) {
    $(modal_name).modal('hide');
    submit_interview_by_id(interview_id, "/api/interviews/", status, sub_status);
  }

  $(document).on('click', '.invite_button', function() {
    resume_selected_value = Number(this.id);
    alert(resume_selected_value);
    tmp_not_support_multi();
  });

  $(document).on('click', '.stage_zero_ai', function() {
    resume_selected_value = Number(this.id);
    show_ai_config_modal(resume_selected_value);
  });

  // TBD: ?
  $(document).on('click', '.stage_zero_sms', function() {
  });

  /*
    About multiple selection
    If the element is for POPUP MODAL, then leave it unchanged.
    If the element is for SUBMIT, then use the multisel* wrapper.
   */
  function do_stage_zero_pass(resume_id) {
    submit_interview_by_compound(resume_id, post_selected_value, "/api/interviews/", 2, '邀约');
  }

  $(document).on('click', '.stage_zero_pass', function() {
    resume_selected_value = Number(this.id);
    multisel_submit_wrapper_resumeid(do_stage_zero_pass);
  });

  function do_stage_zero_fail(resume_id) {
    submit_interview_by_compound(resume_id, post_selected_value, "/api/interviews/", 0, "初选-终止", false);
  }

  $(document).on('click', '.stage_zero_fail', function() {
    resume_selected_value = Number(this.id);
    multisel_submit_wrapper_resumeid(do_stage_zero_fail);
  });

  $(document).on('click', '.stage_one_pass', function() {
    interview_selected_value = Number(this.id);
    $('#nextModal').modal('toggle')
  });

  $(document).on('click', '.stage_one_fail', function() {
    interview_selected_value = Number(this.id);
    resume_id = this.dataset.resume_id;
    show_stop_modal(interview_selected_value, resume_id)
  });

  $(document).on('click', '.stage_two_dail', function() {
    interview_selected_value = Number(this.id);
    resume_id = this.dataset.resume_id;
    // This is a popup
    show_callCandidate_modal(post_selected_value, resume_id);
  });

  $(document).on('click', '.stage_two_pass', function() {
    interview_selected_value = Number(this.id);
    $('#appointmentModal').modal('toggle')
  });
  $(document).on('click', '.stage_two_fail', function() {
    interview_selected_value = Number(this.id);
    resume_id = this.dataset.resume_id;
    show_stop_modal(interview_selected_value, resume_id)
  });

  $(document).on('click', '.stage_three_miss', function() {
    interview_selected_value = Number(this.id);
    resume_id = this.dataset.resume_id;
    show_stop_modal(interview_selected_value, resume_id)
  });
  $(document).on('click', '.stage_three_pass', function() {
    interview_selected_value = Number(this.id);
	resume_id = this.dataset.resume_id;
	  $.ajax({
        url:'/api/resumes/' + resume_id + '/',
        type: 'GET',
		data: null,
		success: function(response) {
		  document.getElementById("text_interview_resumeinfo_username").value = response.username;
		  document.getElementById("text_interview_resumeinfo_phone_number").value = response.phone_number;
        },
		error: function() {
		  console.log("get resume info failed");
		},
	  });
	$('#interviewResultModal').modal('toggle')
  });
  $(document).on('click', '.stage_three_fail', function() {
    interview_selected_value = Number(this.id);
    resume_id = this.dataset.resume_id;
    show_stop_modal(interview_selected_value, resume_id)
  });

  $(document).on('click', '.stage_four_update', function() {
    interview_selected_value = Number(this.id);
	resume_id = this.dataset.resume_id;
	$.ajax({
	  url:'/api/resumes/' + resume_id + '/',
	  type: 'GET',
	  data: null,
      success: function(response) {
	    document.getElementById("text_update_offer_resumeinfo_username").value = response.username;
		document.getElementById("text_update_offer_resumeinfo_phone_number").value = response.phone_number;
      },
	  error: function() {
		console.log("get resume info failed");
	  },
	});
    $('#offerUpdateModal').modal('toggle')
  });
  $(document).on('click', '.stage_four_pass', function() {
    interview_selected_value = Number(this.id);
	resume_id = this.dataset.resume_id;
	$.ajax({
	  url:'/api/resumes/' + resume_id + '/',
	  type: 'GET',
	  data: null,
	  success: function(response) {
		document.getElementById("text_offer_resumeinfo_username").value = response.username;
		document.getElementById("text_offer_resumeinfo_phone_number").value = response.phone_number;
	  },
	  error: function() {
		console.log("get resume info failed");
	  },
	});
    $('#offerModal').modal('toggle')
  });
  $(document).on('click', '.stage_four_fail', function() {
    interview_selected_value = Number(this.id);
    resume_id = this.dataset.resume_id;
    show_stop_modal(interview_selected_value, resume_id)
  });

  $(document).on('click', '.stage_five_update', function() {
    interview_selected_value = Number(this.id);
	resume_id = this.dataset.resume_id;
	$.ajax({
	  url:'/api/resumes/' + resume_id + '/',
	  type: 'GET',
	  data: null,
	  success: function(response) {
		document.getElementById("text_entry_update_resumeinfo_username").value = response.username;
		document.getElementById("text_entry_update_resumeinfo_phone_number").value = response.phone_number;
	  },
	  error: function() {
		console.log("get resume info failed");
	  },
	});
    // This is a popup
    show_entry_update_modal(interview_selected_value);
  });

  $(document).on('click', '.stage_five_pass', function() {
    interview_selected_value = Number(this.id);
	resume_id = this.dataset.resume_id;
	$.ajax({
	  url:'/api/resumes/' + resume_id + '/',
	  type: 'GET',
	  data: null,
	  success: function(response) {
		document.getElementById("text_entry_resumeinfo_username").value = response.username;
		document.getElementById("text_entry_resumeinfo_phone_number").value = response.phone_number;
	  },
	  error: function() {
		console.log("get resume info failed");
	  },
	});
    $('#entryedModal').modal('toggle')
  });

  $(document).on('click', '.stage_five_fail', function() {
    interview_selected_value = Number(this.id);
    resume_id = this.dataset.resume_id;
    show_stop_modal(interview_selected_value, resume_id)
  });

  $(document).on('click', '.stage_six_giveup', function() {
    interview_selected_value = Number(this.id);
    resume_id = this.dataset.resume_id;
    show_stop_modal(interview_selected_value, resume_id)
  });

  $(document).on('click', '.stage_six_pass', function() {
    interview_selected_value = Number(this.id);
	resume_id = this.dataset.resume_id;
	$.ajax({
	  url:'/api/resumes/' + resume_id + '/',
	  type: 'GET',
	  data: null,
	  success: function(response) {
		document.getElementById("text_probation_resumeinfo_username").value = response.username;
		document.getElementById("text_probation_resumeinfo_phone_number").value = response.phone_number;
	  },
	  error: function() {
		console.log("get resume info failed");
	  },
	});
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
      document.getElementById("projectName").innerHTML = tr.innerText;
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

  function do_dial_submit(resume_id) {
    var post_id = post_selected_value;
    var status = 1;

    $.ajax({
      type: "POST",
      url:'/interview/ai/task/',
      data: $('#ai_config_form').serialize(),
    });

    $('#dialModal').modal('hide');

    submit_interview_by_compound(resume_id, post_id, "/api/interviews/", status, 'AI面试');
  }

  $(function(){
    $('#dialFormSubmit').click(function(e){
      e.preventDefault();
      multisel_submit_wrapper_resumeid(do_dial_submit);
    });
  });

  $(function() {
    $('#projSelectorBtn').click(function(e) {
      e.preventDefault();
      $('#projSelector').modal('show')
    });
  });

  function getCurPermSync(post_id) {
      $('#projPermInfo').empty()
      $('#projPermInfo').append("<span>"+"当前的权限分配信息如下:"+"</span>")

      $.ajax({
        url:'/api/permissions/?post_id=' + post_id,
        type: 'GET',
        data: null,
        async: false,
        success: function(response) {
            //console.log("response ", response)
            $.each(response.results, function(index, ele) {
                $('#projPermInfo').append('<span style="display:block">'+ele.stage_name + ':' + ele.user_name + '</span>')
            });
        },
        error: function() {
            console.log("get resume info failed");
            alert('Sth Wrong')
        },
      });
  }

  $('#permOp').change(function(e) {
      var stage = $('#interview_stage_id').val()
      var who = $('#cRecruiter').val()
      var op = $('#permOp').val()
      var fields = 'post=' + post_selected_value + '&user=' + who + '&stage=' + stage
      $('#permOp').val("")
	  $('#interview_stage_id').val("")
      $('#cRecruiter').val("")
	  data = {
		"post": post_selected_value,
		"user": who,
		"stage": stage,
	  }
      if (op=="增加") {
	    xhr_common_send('POST', '/api/permissions/', data)
      } else if (op == "删除") {
        // step1: get the item
        $.ajax({
            url:'/api/permissions/?post=' + post_selected_value + '&user=' + who + '&stage=' + stage,
            type: 'GET',
            data: null,
            success: function(response) {
                console.log('/api/permissions/?post=' + post_selected_value + '&user=' + who + '&stage=' + stage)
                $.each(response.results, function(index, ele) {
                    console.log("index: ", index, " ", ele.id)
	                xhr_common_send('DELETE', '/api/permissions/'+ele.id+'/', null)
                });
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('api/permissions/?post=' + post_selected_value + '&user=' + who + '&stage=' + stage)
				console.log(jqXHR.responseText);
                console.log(jqXHR.status);
				console.log(jqXHR.readyState);
                console.log(jqXHR.statusText);
                console.log(textStatus);
                console.log(errorThrown);
                alert('Sth Wrong')
            },
        });
      }
      getCurPermSync(post_selected_value)
		/*
      $.ajax({
        url:'/api/permissions/' ,
        type: 'POST',
        data: fields,
        success: function(response) {
            getCurPermSync(post_selected_value)
        },
        error: function(jqXHR, textStatus, errorThrown) {
				console.log(jqXHR.responseText);
                console.log(jqXHR.status);
				console.log(jqXHR.readyState);
                console.log(jqXHR.statusText);
                console.log(textStatus);
                console.log(errorThrown);

            alert('Sth Wrong')
        },
      });
		*/
  });

  function getRecruiterSync() {
      $('#cRecruiter').html("")
      $('#cRecruiter').prepend('<option value=""></option>')
      $.ajax({
        url:'/api/accounts/?user_type=Recruiter' ,
        type: 'GET',
        async: false,
        data: null,
        success: function(response) {
          $.each(response.results, function(index, ele){
              $('#cRecruiter').append('<option value=' + ele.id + '>' + ele.username + '</option>')
          })
        },
        error: function(response) {
            console.log("get resume info failed");
            alert('Sth Wrong')
        },
      });
  }

  $(function() {
    $('#projPermissionBtn').click(function(e) {
      e.preventDefault();
      // step0: Get the all recruiter
      // step1: First should update the header
      $.ajax({
        url:'/api/posts/' + post_selected_value + '/',
        type: 'GET',
        data: null,
        success: function(response) {
            // get the project info successfully
            // then to get the project info
            $('#projPermName').text(response.name)
            $('#permOp').val("")
            $('#interview_stage_id').val("")
            getRecruiterSync()
            getCurPermSync(post_selected_value)
            $('#projPermission').modal('show')
        },
        error: function() {
            console.log("get resume info failed");
            alert('Sth Wrong')
        },
      });
      // step2: Then the all recruiter

    });
  });

  function do_next_submit(interview_id) {
    var status = 2;
    $('#nextModal').modal('hide');
    submit_interview_by_id(interview_id, "/api/interviews/", status, '邀约');
  }

  $(function() {
    $('#nextSubmit').click(function(e){
      e.preventDefault();
      multisel_submit_wrapper(do_next_submit);
    });
  });

  function do_stop_submit(interview_id) {
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
  }

  $(function() {
    $('#stopFormSubmit').click(function(e){
      e.preventDefault();
      multisel_submit_wrapper(do_stop_submit);
    });
  });

  function do_interviewResult_submit(interview_id) {
    $('#interviewResultModal').modal('hide');
    //var status = 4;
    data = {
      "interview_sub": {
        "interview": interview_id,
        "result_type": 3
      },
      "comments": helper_get_textbox_text("text_interviewresult_comments"),
    };

    submit_interviewsub_by_id("/interviews/api/interview_sub_pass/", table, data);
  }

  $(function() {
    $('#interviewResultFormSubmit').click(function(e){
      e.preventDefault();
      multisel_submit_wrapper(do_interviewResult_submit);
    });
  });

  function do_offerInfo_submit(interview_id) {
    $('#offerModal').modal('hide');
    //var status = 5;

    data = {
      "offer_sub": {
        "interview": interview_id,
        "result_type": 3
      },
      "op": "UpdatePass",
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
  }

  function do_offerInfoUpdate_submit(interview_id) {
    $('#offerUpdateModal').modal('hide');
    data = {
      "offer_sub": {
        "interview": interview_id,
        "result_type": 3
      },
      "op": "Update",
      "date": helper_get_textbox_text("text_update_offerinfo_date"),
      "contact": helper_get_textbox_text("text_update_offerinfo_contact"),
      "contact_phone": helper_get_textbox_text("text_update_offerinfo_contact_phone"),
      "address": helper_get_textbox_text("text_update_offerinfo_address"),
      "postname": helper_get_textbox_text("text_update_offerinfo_postname"),
      "certification": helper_get_textbox_text("text_update_offerinfo_certification"),
      "salary": helper_get_textbox_text("text_update_offerinfo_salary"),
      "notes": helper_get_textbox_text("text_update_offerinfo_notes")

    };
    submit_interviewsub_by_id("/interviews/api/offer_sub_agree/", table, data);
  }

  $(function(){
    $('#offerSubmit').click(function(e){
      e.preventDefault();
      multisel_submit_wrapper(do_offerInfo_submit);
    });
  });

  $(function() {
    $('#offerUpdateSubmit').click(function(e) {
      e.preventDefault();
      multisel_submit_wrapper(do_offerInfoUpdate_submit);
    });
  });

  function do_entryed_submit(interview_id) {
    do_common_plain_submit(interview_id, '#entryedModal', 6, '考察');
  }

  $(function(){
    $('#entryedSubmit').click(function(e){
      e.preventDefault();
      multisel_submit_wrapper(do_entryed_submit);
    });
  });

  function do_entryUpdate_submit(interview_id) {
    $('#entryUpdateModal').modal('hide');
    //var status = 5;

    data = {
      "offer_sub": {
        "interview": interview_id,
        "result_type": 4
      },
      "op":"Update",
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
  }

  $(function(){
    // only update the entry info
    $('#entryUpdateSubmit').click(function(e){
      e.preventDefault();
      multisel_submit_wrapper(do_entryUpdate_submit);
    });
  });

  function do_probationSucc_submit(interview_id) {
    do_common_plain_submit(interview_id, '#probationSuccModal', 7, '回款');
  }

  $(function(){
    // only update the entry info
    $('#probationSuccSubmit').click(function(e){
      e.preventDefault();
      multisel_submit_wrapper(do_probationSucc_submit);
    });
  });

  function do_probationFail_submit(interview_id) {
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
  }

  $(function(){
    // only update the entry info
    $('#probationFailSubmit').click(function(e){
      e.preventDefault();
      multisel_submit_wrapper(do_probationFail_submit);
    });
  });

  function do_pbInvoice_submit(interview_id) {
    do_common_plain_submit(interview_id, '#pbInvoiceModal', 7, '回款');
  }

  $(function(){
    // only update the entry info
    $('#pbInvoiceSubmit').click(function(e){
      e.preventDefault();
      multisel_submit_wrapper(do_pbInvoice_submit);
    });
  });

  function do_pbBaddebt_submit(interview_id) {
    do_common_plain_submit(interview_id, '#pbBaddebtModal', 7, '坏账');
  }

  $(function(){
    // only update the entry info
    $('#pbBaddebtSubmit').click(function(e){
      e.preventDefault();
      multisel_submit_wrapper(do_pbBaddebt_submit);
    });
  });

  function do_pbFinish_submit(interview_id) {
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
  }

  $(function(){
    // only update the entry info
    $('#pbFinishSubmit').click(function(e){
      e.preventDefault();
      multisel_submit_wrapper(do_pbFinish_submit);
    });
  });

  function do_pbRegister_submit(interview_id) {
    do_common_plain_submit(interview_id, '#pbRegisterModal', 7, '已经注册');
  }

  $(function(){
    // only update the entry info
    $('#pbRegisterSubmit').click(function(e){
      e.preventDefault();
      multisel_submit_wrapper(do_pbRegister_submit);
    });
  });

  function do_appointment_submit(interview_id) {
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
  }
  $(function() {
    $('#appointmentSubmit').click(function(e){
      e.preventDefault();
      multisel_submit_wrapper(do_appointment_submit);
    });
  });

  // ================================================================================
  $(function() {
    $('#agree_interview').click(function(e){
      $('#dailToCandidateModal').modal('hide');
      $('#appointmentModal').modal('show');
    });
  });

  function do_dial_deeper_submit(interview_id) {
    var status = 2;
    $('#dailToCandidateModal').modal('hide');
    submit_interview_by_id(interview_id, "/api/interviews/", status, '深度沟通');
  }

  $(function() {
    $('#dail_deeper_communicate').click(function(e){
      e.preventDefault();
      multisel_submit_wrapper(do_dial_deeper_submit);
    });
  });

  function do_dial_not_linked_submit(interview_id) {
    var status = 2;
    $('#dailToCandidateModal').modal('hide');
    submit_interview_by_id(interview_id, "/api/interviews/", status, '未接通');
  }

  $(function() {
    $('#dail_not_linked').click(function(e){
      e.preventDefault();
      multisel_submit_wrapper(do_dial_not_linked_submit);
    });
  });

  $(function() {
    $('#giveup_interview').click(function(e){
      $('#dailToCandidateModal').modal('hide');
      resume_id = this.dataset.resume_id;
      show_stop_modal(interview_selected_value, resume_id)
    });
  });

  // ================================ CLICKS END ================================================
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
