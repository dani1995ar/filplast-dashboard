window.onload = function() {
  let input = document.getElementById('full-name');
  input.addEventListener('keyup', function() {
    if(input.value.length == 3) {
      $.get('/search?type=suggestion&q=' + input.value).done(function(data) {
        $('#full-name').autocomplete({
            source: data,
            minLength: 3
        });
      });
    }
  });
}
