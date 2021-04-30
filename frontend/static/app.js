$(document).ready(() => {
  $('#image-file-input').change(function() {
    let filename = $(this).val().split('\\').pop();
    $('#image-path-label').text(filename).removeClass('text-muted');
  });

  $('#upload-reset-button').click(function() {
    $('#image-path-label').text('Choose file').addClass('text-muted');
  });

  $('.upload-form').submit(function() {
    //return false;
  });
});
