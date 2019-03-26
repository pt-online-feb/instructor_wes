$(document).ready(function() {
  $.get('/users/first_name', function(firstName) {
    $('#user-first-name').html(firstName);
  })

  $.get('/resume_items/' + CURRENT_USER_ID, function(items) {
    $('#resume-items').html(items);
  })
  
  $("#item-create-form").submit(function(e) {
    e.preventDefault()
    $.ajax({
      url: '/resume_items/create',
      method: 'POST',
      data: $('#item-create-form').serialize(),
      success: function() {
        $.get('/resume_items/' + CURRENT_USER_ID, function (items) {
          $('#resume-items').html(items);
        })
        $('#item-create-form input, #item-create-form textarea').val("")
      },
      error: function(data) {
        $("#errors").html(data.responseText)
      }
    })
  })
})