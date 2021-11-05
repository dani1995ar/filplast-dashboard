window.onload = function() {
  let input = document.getElementById('full-name');
  input.addEventListener('keyup', function() {
    $.get('/search?type=suggestion&q=' + input.value).done(function(data) {
      $('#full-name').autocomplete({
          source: data,
          minLength: 3
      });
    });
  });
}
