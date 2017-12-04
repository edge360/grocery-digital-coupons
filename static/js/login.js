$(function() {
  $('form').submit(function(e) {
    $('#error').text('').addClass('invisible');

    // Get a token from /api/login
    $.ajax({
        type: 'POST',
        url: '/api/login',
        contentType: 'application/json',
        data: JSON.stringify({ username: $('#username').val(), password: $('#password').val() }),
        success: function(data) {
          if (!data.error) {
            document.location = '/?token=' + data.token;
          }
          else {
            $('#error').text(data.error).removeClass('invisible');
          }
        }
    });
  });
});