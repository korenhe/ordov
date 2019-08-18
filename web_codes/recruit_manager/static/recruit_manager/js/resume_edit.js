var resume_id = -1
$(document).ready(function() {
    resume_basic_op(readonly=true)
    // get the resume id from the original url
    // TODO: not so strong here
    var component=(window.location.href.split("/"))
    resume_id = component[5]
    console.log("id", resume_id)
    get_resume_basic()
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
            print("Fail to get resume info of ", resume_id)
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
