function param(name) {
    return (location.search.split(name + '=')[1] || '').split('&')[0];
}

$(function() {
  onInitialize();
});

var onStatus = function(init) {
  // Get status from /api/status?token=
  $.ajax({
      type: 'GET',
      url: '/api/status?token=' + param('token'),
      contentType: 'application/json',
      success: function(data) {
        if (!data.error) {
          $('#result').removeClass('d-none');
          $('#logout').removeClass('d-none');
          $('#progress').removeClass('d-none');

          // Render status.
          $('#resultTitle').text(data.username);
          $('#existingCount').text(data.existingCount || 0);
          $('#count').text(data.count || 0);
          $('#status').text(data.status || 'None');
          $('#message').text(data.message);
          $('#startDate').text(data.startDate);

          var message = '';
          if (data.endDate) {
            $('#progress').addClass('d-none');
            message = 'Completed';
          }
          else {
            message = 'Updated';

            // Continue refresh.
            setTimeout(function() {
              onStatus();
            }, 2000);
          }

          message += ' on ' + data.endDate || data.lastUpdate;
          $('#endDate').text(message);

          if (data.screenshot) {
            $('#screenshot').html('<img class="card-img-bottom img-thumbnail" src="data:image/png;base64,' + data.screenshot + '" alt="Result">');
          }
        }
        else {
          $('#error').text(data.error).removeClass('invisible');
        }
      },
      error: function(data, status, message) {
        var message = 'Error loading status. ' + (data.responseJSON ? data.responseJSON.error : message);
        console.error(message);
        $('#error').text(message).removeClass('d-none');

        if (init) {
          document.location = '/login';
        }
      }
  });
}

var onInitialize = function() {
  $('#logout').click(function() {
    $.ajax({
      type: 'DELETE',
      url: '/api/status?token=' + param('token'),
      contentType: 'application/json',
      success: function(data) {
        console.log(data);
        window.location = '/login';
      },
      error: function(data, status, message) {
        var message = 'Error logging out. ' + (data.responseJSON ? data.responseJSON.error : message);
        console.error(message);
        
        document.location = '/login';
      }
    });
  });

  // Render status and start refresh.
  onStatus(true);
}