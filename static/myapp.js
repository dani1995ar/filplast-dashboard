window.onload = function() {
  let input = document.getElementById('full-name');
  input.addEventListener('keyup', function() {
    $.get('/search?type=suggestion&q=' + input.value, function(suggestion) {
      let html = '';
      for (any in suggestion) {
        let name = suggestion[any];
        html += '<li>' + name + '</li>'; 
      }
      document.getElementById('full-name-suggestion').innerHTML = '<ul>' + html + '</ul>';
    });
  });
};