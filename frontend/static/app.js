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
        return Math.round(elapsed/msPerYear ) + 'yr';   
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
}

function refreshImageList() {
  $('#image-list-spinner').show();
  let d1 = new Date();
  let currentTime = new Date(
    d1.getUTCFullYear(), 
    d1.getUTCMonth(), 
    d1.getUTCDate(), 
    d1.getUTCHours(), 
    d1.getUTCMinutes(), 
    d1.getUTCSeconds()
  );

  $.ajax({
    url: '/api/list_images',
    success: function(data) {
      let html = '';
      for (i = 0; i < data.count; ++i) {
        let item = data.data[i];
        let timeDiff = timeDifference(currentTime, item.timestamp * 1000);
        html += `
        <div class="col-md-4">
          <div class="card mb-4 box-shadow">
            <img class="card-img-top" src="${item.image_url}">
            <div class="card-body">
              <p class="card-text">Uploaded by <b>${item.username}</b></p>
              <div class="d-flex justify-content-between align-items-center">
                <span class="badge badge-primary">${item.filter_used}</span>
                <small class="text-muted">${timeDiff} ago</small>
              </div>
            </div>
          </div>
        </div>`;
      }

      $('#image-list').html(html);
      $('#image-list-spinner').hide();
    }
  });
}

$(document).ready(() => {
  $('#image-file-input').change(function() {
    let filepath = $(this).val();
    if (filepath.length == 0) {
      resetUploadInput();
      return;
    }

    let filename = filepath.split('\\').pop();
    $('#image-path-label').text(filename).removeClass('text-muted');

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

  $('.upload-form').submit(function() {
    // validate
    

    //return false;
  });

  refreshImageList();
});
