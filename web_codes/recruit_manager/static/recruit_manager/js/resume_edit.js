var resume_id = -1
var experience_id = -1
$(document).ready(function() {
    resume_basic_op(readonly=true)
    // get the resume id from the original url
    // TODO: not so strong here
    var component=(window.location.href.split("/"))
    resume_id = component[5]
    console.log("id", resume_id)
    get_resume_basic()
    get_resume_experience()
});

$(document).on('click', '#resume_basic_edit_button', function() {
    resume_basic_op(false)
    get_resume_basic()
    // ajax to get the resume info
});

function get_resume_basic() {
    $.ajax({
        url: '/api/resumes/' + resume_id + '/',
        type: 'GET',
        data: null,
        success: function(response) {
            console.log(response)
            console.log(response.email)
           gender = '男'
           if (response.gender == 'f') {
               gender = '女'
           }
           $('#resume_basic_name').val(response.username)
           $('#resume_basic_gendor').val(gender)
           $('#resume_basic_birth_time').val("")
           $('#resume_basic_work_time').val("")
           $('#resume_basic_birth_place').val(response.birthorigin)
           $('#resume_basic_current_place').val("xiaoming")
           $('#resume_basic_phone').val(response.phone_number)
           $('#resume_basic_email').val(response.email)
           $('#resume_basic_role').val()
        },
        error: function() {
            console.log("Fail to get resume info of ", resume_id)
        }
    })
}

function get_resume_experience() {
    console.log('/api/experiences?resume_id=' + resume_id)
    $.ajax({
        // Keep the standard restful API here
        url: '/api/experiences?resume_id=' + resume_id,
        type: 'GET',
        data: null,
        success: function(response) {
            console.log(response)
            $.each(response.results, function(index, ele) {
                console.log("exp.end:", ele.end, " company:", ele.company_name, " ele.id:", ele.id)
                $('#resume_experience_show').append(
                    '<div class="resume_experience_item" id=' + ele.id + '>' +
                    '<div class="row">' +
                      '<div class="col-md-3">' +
                        ele.start + ' -- ' + ele.end +
                      '</div>' +
                      '<div class="col-md-4">' +
                        ele.company_name +
                      '</div>' +
                      '<div class="col-md-4">' +
                        ele.post_name +
                      '</div>' +
                      '<div class="col-md-1">' +
                        '<i class="fas fa-edit resume_experience_edit_button" id=' + ele.id + ' style=""></i>' +
                      '</div>' +
                    '</div>' +
                    '</div>'

                )
                $('#resume_experience_show').append(
                    '<div class="resume_experience_item_edit" id=' + ele.id + ' style="display:none;">' +
                    '<div class="row">' +
                      '<div class="col-md-6 input-group">' +
                        '<div class="input-group-prepend resume_basic_addon">' +
                          '<span class="input-group-text resume_basic_header1" id="basic-addon1">开始时间</span>' +
                        '</div>' +
                        '<input type="text" class="form-control" name="resume_basic_name" id="experience_start" value="">' +
                      '</div>' +
                      '<div class="col-md-6 input-group">' +
                        '<div class="input-group-prepend resume_basic_addon">' +
                          '<span class="input-group-text resume_basic_header1" id="basic-addon1">结束时间</span>' +
                        '</div>' +
                        '<input type="text" class="form-control" name="resume_basic_name" id="experience_end" value="">' +
                      '</div>' +
                    '</div>' +
                    '<div class="row">' +
                      '<div class="col-md-6 input-group">' +
                        '<div class="input-group-prepend resume_basic_addon">' +
                          '<span class="input-group-text resume_basic_header1" id="basic-addon1">公司名</span>' +
                        '</div>' +
                        '<input type="text" class="form-control" name="resume_basic_name" id="experience_company_name" value="">' +
                      '</div>' +
                      '<div class="col-md-6 input-group">' +
                        '<div class="input-group-prepend resume_basic_addon">' +
                          '<span class="input-group-text resume_basic_header1" id="basic-addon1">职位名</span>' +
                        '</div>' +
                        '<input type="text" class="form-control" name="resume_basic_name" id="experience_post_name" value="">' +
                      '</div>' +
                    '</div>' +
                    '<div class="row">' +
                      '<div class="col-md-6 input-group">' +
                        '<div class="input-group-prepend resume_basic_addon">' +
                          '<span class="input-group-text resume_basic_header1" id="basic-addon1">职责</span>' +
                        '</div>' +
                        '<input type="text" class="form-control" name="resume_basic_name" id="experience_duty" value="">' +
                      '</div>' +
                      '<div class="col-md-6 input-group">' +
                        '<div class="input-group-prepend resume_basic_addon">' +
                          '<span class="input-group-text resume_basic_header1" id="basic-addon1">薪水</span>' +
                        '</div>' +
                        '<input type="text" class="form-control" name="resume_basic_name" id="experience_salary" value="">' +
                      '</div>' +
                    '</div>' +
                    '<div class="row">' +
                      '<div class="col-md-12 input-group">' +
                        '<div class="input-group-prepend resume_basic_addon">' +
                          '<span class="input-group-text resume_basic_header1" id="basic-addon1">描述</span>' +
                        '</div>' +
                        '<input type="text" class="form-control" name="resume_basic_name" id="experience_description" value="">' +
                      '</div>' +
                    '</div>' +
                    '<div class="row">' +
                      '<div class="col-md-6">' +
                        '<button type="button" class="experience_save" id=' + ele.id + '>' +
                          '确定' +
                        '</button>' +
                      '</div>' +
                      '<div class="col-md-6">' +
                        '<button type="button" class="experience_cancel" id=' + ele.id + '>' +
                          '取消' +
                        '</button>' +
                      '</div>' +
                    '</div>' +
                    '</div>'
                )
                $('div[class="resume_experience_item_edit"][id=' + ele.id + '] #experience_start').val(ele.start)
                $('div[class="resume_experience_item_edit"][id=' + ele.id + '] #experience_end').val(ele.end)
                $('div[class="resume_experience_item_edit"][id=' + ele.id + '] #experience_company_name').val(ele.company_name)
                $('div[class="resume_experience_item_edit"][id=' + ele.id + '] #experience_post_name').val(ele.post_name)
                $('div[class="resume_experience_item_edit"][id=' + ele.id + '] #experience_description').val(ele.experience_description)
                $('div[class="resume_experience_item_edit"][id=' + ele.id + '] #experience_salary').val(ele.salary)
            })
        },
        error: function() {
           console.log("Fail to get the experience of ", resume_id)
        }
    })
}

$(document).on('click', '#resume_basic_edit_cancel', function() {
    resume_basic_op(readonly=true)
});

$(document).on('click', '#resume_basic_edit_confirm', function() {
});

$(document).on('click', '#resume_basic_edit_button_down', function() {
   $('#resume_basic_show').css('display', 'none')
   $('#resume_basic_edit_button_up').css('display', 'inline')
   $('#resume_basic_edit_button_down').css('display', 'none')
});

$(document).on('click', '#resume_basic_edit_button_up', function() {
   $('#resume_basic_show').css('display', 'inline')
   $('#resume_basic_edit_button_up').css('display', 'none')
   $('#resume_basic_edit_button_down').css('display', 'inline')
});

function resume_basic_op(readonly) {
    if (readonly) {
        $('#resume_basic_name').attr('readonly', true)
        $('#resume_basic_gendor').attr('readonly', true)
        $('#resume_basic_birth_time').attr('readonly', true)
        $('#resume_basic_work_time').attr('readonly', true)
        $('#resume_basic_birth_place').attr('readonly', true)
        $('#resume_basic_current_place').attr('readonly', true)
        $('#resume_basic_phone').attr('readonly', true)
        $('#resume_basic_email').attr('readonly', true)
        $('#resume_basic_role').attr('readonly', true)
        $('#resume_basic_edit_confirm').css('display', 'none')
        $('#resume_basic_edit_cancel').css('display', 'none')
    } else {
        $('#resume_basic_name').attr('readonly', false)
        $('#resume_basic_gendor').attr('readonly', false)
        $('#resume_basic_birth_time').attr('readonly', false)
        $('#resume_basic_work_time').attr('readonly', false)
        $('#resume_basic_birth_place').attr('readonly', false)
        $('#resume_basic_current_place').attr('readonly', false)
        $('#resume_basic_phone').attr('readonly', false)
        $('#resume_basic_email').attr('readonly', false)
        $('#resume_basic_role').attr('readonly', false)
        $('#resume_basic_edit_confirm').css('display', 'inline')
        $('#resume_basic_edit_cancel').css('display', 'inline')
    }
}

$(document).on('click', '.resume_experience_edit_button', function() {
   var id = Number(this.id)
   console.log('[class="resume_experience_item_edit"][id=' + id + ']')
   // get the specified resume_id/experience_id info
   // Attention: the and logic for jquery
   $('div[class="resume_experience_item_edit"][id=' + id + ']').show()
});

$(document).on('click', '.resume_experience_item_edit .experience_save', function() {
    var id= Number(this.id)
    // update the resume info
    alert(id)
});
$(document).on('click', '.resume_experience_item_edit .experience_cancel', function() {
    var id= Number(this.id)
    $('div[class="resume_experience_item_edit"][id=' + id + ']').css('display','none')
});
