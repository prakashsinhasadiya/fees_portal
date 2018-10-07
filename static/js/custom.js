$(document).ready(function() {

  $("#institute").change(function (event) {
    var institute = $("#institute option:selected").attr('value')
    debugger;
    data = {'institute':institute}
    $.ajax({
            type: "POST",
            data: data,            
            dataType: 'JSON',
            url: /get_branch/,
        success: function (response) {
          $('#branch').find('option').remove()
          var result = JSON.parse(response['response']);
          $.each( result, function( key, value ) {
            debugger;
            var text = value['name']
            var value_id = value['id']
            $("#branch").append(new Option(text, value_id));
          });
        }
      })
  
} )
} );

