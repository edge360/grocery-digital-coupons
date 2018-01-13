$(() => {
  onInitialize();
});

var onStatus = function(init) {
  // Get status from /api/status?token=
  $.ajax({
      type: 'GET',
      url: '/api/status',
      contentType: 'application/json',
      headers: {
        'token': sessionStorage['token']
      },
      success: data => {
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

        let message = '';
        if (data.endDate) {
          $('#progress').addClass('d-none');
          message = 'Completed';
        }
        else {
          message = 'Updated';

          // Continue refresh.
          setTimeout(() => {
            onStatus();
          }, 2000);
        }

        const date = data.endDate || data.lastUpdate;
        message += ' on ' + date;
        $('#endDate').text(date ? message : '');
        if (!data.endDate) {
          let lastRefresh = new Date() + '';
          const index = lastRefresh.indexOf('GMT');
          lastRefresh = lastRefresh.substring(0, index + 3);
          $('#lastRefresh').text(`Refreshed on ${lastRefresh}`);
        }
        else {
          $('#lastRefresh').text('');
        }

        if (data.screenshot) {
          $('#screenshot').html(`<img class='card-img-bottom img-thumbnail' src='data:image/png;base64,${data.screenshot}' alt='Result'>`);
        }

        if (data.error) {
          $('#error').text(data.error).removeClass('d-none');
        }
      },
      error: (data, status, message) => {
        const str = data.responseJSON ? data.responseJSON.error : message;

        message = `Error loading status. ${str}`;
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
      url: '/api/status',
      contentType: 'application/json',
      headers: {
        'token': sessionStorage['token']
      },
      success: data => {
        sessionStorage.removeItem('token');
        
        console.log(data);
        window.location = '/login';
      },
      error: (data, status, message) => {
        const str = data.responseJSON ? data.responseJSON.error : message;

        message = `Error logging out. ${str}`;
        console.error(message);
        
        document.location = '/login';
      }
    });
  });

  // Render status and start refresh.
  onStatus(true);
}