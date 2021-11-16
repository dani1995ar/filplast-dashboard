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

  const maxInputs = 9; // Max amount of order items per order (i.e. pla azul, abs negro, tpu naranja...)
  let orderItemsWrapper = $('#orderItemsInputWrapper'); // Order item inputs div
  let addItemsButton = $('#addProductAndAmount'); // "+" next to amount input
  let products = document.getElementById('product-id').innerHTML;

  let orderItemsCount = orderItemsWrapper.length; // Amount of order items input div
  let fieldCount = 1; // Track of total added fields
  $(addItemsButton).click(function(e) {
    if(orderItemsCount <= maxInputs){
      let htmlProductAndAmount = 
      '<div class="moreItemsWrapper">' +
        '<div class="col">' +
        '<div class="form-group">' +
          '<label for="product-id">Select product name:</label>' +
          '<select name="product-id' + fieldCount + '" id="product-id' + fieldCount + '" required>' +
            products +
          '</select>' +
        '</div>' +
      '</div>' +
      '<div class="col">' +
        '<div class="form-group">' +
          '<label for="quantity">Amount of product:</label>' +
          '<input type="number" placeholder="quantity" name="quantity' + fieldCount + '" min="1" required>' +
          '<button type="button" name="removeProductAndAmount" id="removeProductAndAmount" class="btn btn-success">-</button>' +
        '</div>' +
      '</div>' +
      '</div>';
      fieldCount++;
      $(orderItemsWrapper).append(htmlProductAndAmount);
      orderItemsCount++;
    }
    else {
      alert('You\'ve reached the maximum amount of fields you can have, contact the developer for more info');
    }
    return false;
  })

  // Remove fields function
  $("body").on("click","#removeProductAndAmount", function(e) { 
    if( orderItemsCount > 1 ) {
            // Remove inputs
            $(this).closest('.moreItemsWrapper').remove();
            // Decrement count
            orderItemsCount--;
    }
    return false;
  })
}