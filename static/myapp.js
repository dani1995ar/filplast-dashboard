$(function() {
    $('input#create-order-full-name').keyup(function() {
      $.getJSON('/create-order-search', {
        fullName : $('#create-order-full-name').val()
      }, function(data) {
        $('#full-name-suggestion').text(data.fullName);
      });
      return false;
    });
  });