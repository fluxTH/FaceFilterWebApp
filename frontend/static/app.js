function timeDifference(current, previous) {

    var msPerMinute = 60 * 1000;
    var msPerHour = msPerMinute * 60;
    var msPerDay = msPerHour * 24;
    var msPerMonth = msPerDay * 30;
    var msPerYear = msPerDay * 365;

    var elapsed = current - previous;

    if (elapsed < msPerMinute) {
         return Math.round(elapsed/1000) + 's';   
    }

    else if (elapsed < msPerHour) {
         return Math.round(elapsed/msPerMinute) + 'm';   
    }

    else if (elapsed < msPerDay ) {
         return Math.round(elapsed/msPerHour ) + 'h';   
    }

    else if (elapsed < msPerMonth) {
        return Math.round(elapsed/msPerDay) + 'd';   
    }

    else if (elapsed < msPerYear) {
        return Math.round(elapsed/msPerMonth) + 'mo';   
    }

    else {
        return Math.round(elapsed/msPerYear ) + 'y';   
    }
}

function readImageFile(input, cb) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    
    reader.onload = cb;    
    reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}

function resetUploadInput() {
  $('#image-path-label').text('Choose file').addClass('text-muted');
  $('#upload-preview').hide();
  clearError();
}

function refreshImageList(showSpinner) {
  if (showSpinner !== false)
    $('#image-list-spinner').show();

  let currentTime = new Date();

  let errorTail = '. Please try again later.';

  $.ajax({
    url: '/api/list_images',
    success: function(data) {
      if (data.status == 'success') {
        clearILError();
        let html = '';

        if (data.count > 0) {
          for (i = 0; i < data.count; ++i) {
            let item = data.data[i];
            let d = Date.parse(item.timestamp);
            let timeDiff = timeDifference(currentTime, d);
            html += `
            <div class="col-md-4">
              <div class="card mb-4 box-shadow">
                <a href="${item.image_url}" target="_blank"><img class="card-img-top" src="${item.image_url}"></a>
                <div class="card-body">
                  <p class="card-text">Uploaded by <b>${item.username}</b></p>
                  <div class="d-flex justify-content-between align-items-center">
                    <span class="badge badge-primary"><i class="fas fa-magic"></i> ${item.filter_used}</span>
                    <span class="badge badge-secondary"><i class="far fa-smile-wink"></i> ${item.face_count}</span>
                    <small class="text-muted">${timeDiff} ago</small>
                  </div>
                </div>
              </div>
            </div>`;
          }
        } else {
          html += '<p class="text-muted">No uploaded images.</p>';
        }

        $('#image-list').html(html);
        $('#image-list-spinner').hide();
        return;
      }

      if (data.status == 'error') {
        showILError(data.message);
        return;
      }

      showILError('Unknown Error');
    },
    error: function(o, e, es) {
      if (es == '') es = o.statusCode; 
      showILError(e + ' ' + es);
    }
  });
}

function showError(msg) {
  $('#upload-error-alert').find('span.error-message').text(msg);
  $('#upload-error-alert').show();
}

function clearError() {
  $('#upload-error-alert').hide();
}

function showILError(msg) {
  $('#imagelist-error-alert').find('span.error-message').text(msg);
  $('#imagelist-error-alert').show();
}

function clearILError() {
  $('#imagelist-error-alert').hide();
}
function showUploadStatus() {
  $('.upload-form-button').attr('disabled', 'disabled');
  $('#upload-submit-button').html('<i class="fa fa-spinner fa-spin"></i> Uploading...');
}

function resetUploadStatus() {
  $('.upload-form-button').removeAttr('disabled');
  $('#upload-submit-button').html('<i class="fas fa-cloud-upload-alt"></i> Upload!');
}

$(document).ready(() => {
  $('#image-file-input').change(function() {
    let filepath = $(this).val();
    if (filepath.length == 0) {
      resetUploadInput();
      return;
    }

    let filename = filepath.split('\\').pop();
    let extension = filename.split('.').pop();
    if (!['png', 'jpg', 'jpeg'].includes(extension)) {
      alert('Only image files with extension "jpg", "png" and "jpeg" are allowed.');
      $(this).val(null);
      return;
    }

    $('#image-path-label').text(filename).removeClass('text-muted');

    clearError();

    $('#upload-preview').hide();
    $('#upload-spinner').show();

    readImageFile(this, function(e) {
      $('#upload-spinner').hide();
      $('#upload-preview').attr('src', e.target.result).show();
    });
  });

  $('#upload-reset-button').click(function() {
    resetUploadInput();
  });

  $('#upload-return-button').click(function() {
    $('#upload-reset-button').click();
    $('.result-view').hide();
    $('.upload-form').show();
    window.scrollTo(0, 0);
    return false;
  });

  $('.upload-form').submit(function() {
    clearError();
    showUploadStatus();

    let usernameInput = $('input[name=username]');
    if (usernameInput.val().length == 0) {
      $(usernameInput).val('Anonymous');
    }

    let formData = new FormData(this);
    $.ajax({
      url: '/api/upload',
      type: 'POST',
      cache: false,
      contentType: false,
      processData: false,
      data: formData,
      success: function(data) {
        window.scrollTo(0, 0);
        resetUploadStatus();

        if (data.status == 'success') {
          $('#image-result').attr('src', data.image_url);
          $('.result-view').show();
          $('.upload-form').hide();

          refreshImageList();
          return;
        }

        if (data.status == 'error') {
          showError(data.message);
          return;
        }

        showError("An unknown error occurred");
        return;
      },
      error: function(o, e, es) {
        window.scrollTo(0, 0);
        resetUploadStatus();
        if (es == '') es = o.statusCode; 
        showError(es);
      }
    });

    return false;
  });

  refreshImageList();

  setInterval(function() {
    refreshImageList(false);
  }, 10000);
});
