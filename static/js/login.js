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
            sessionStorage['token'] = data.token;
            document.location = '/';
          }
          else {
            $('#error').text(data.error).removeClass('invisible');
          }
        },
        error: function(data, status, message) {
          console.error('Error logging in: ' + status + ' ' + message);
          console.error(data);
        }
    });

    e.preventDefault();
    return false;
  });
});