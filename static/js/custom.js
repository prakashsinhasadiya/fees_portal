$(document).ready(function() {

  $("#institute").change(function (event) {
    var institute = $("#institute option:selected").text()
    data = {'institute':institute}
    $.ajax({
            type: "POST",
            data: data,            
            dataType: 'JSON',
            url: /get_branch/,
        success: function (response) {
          debugger;
        }
      })
  
} )
} );

