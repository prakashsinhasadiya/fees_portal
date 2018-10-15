$(document).ready(function() {

  $("#institute").change(function (event) {
    var institute = $("#institute option:selected").attr('value')
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
            var text = value['name']
            var value_id = value['id']
            $("#branch").append(new Option(text, value_id));
          });
        }
      })
  
} )
  $(".custome-name").focusin(function(){
    debugger
    $(".custom-error").remove();
});
  $(".checkbox").on("click",function (event) {
    var value = $(this).find('#fees_type_id').attr('value')
    var selected = $(this).find('#fees_type_id')[0].checked
    var branch = $("#branch").attr('value')
    var amount_value = $('#float_value').attr('value')
    data = {'value':value,'selected':selected,'branch':branch,'amount_value':amount_value}
    $.ajax({
            type: "POST",
            data: data,            
            dataType: 'JSON',
            url: /amount_value/,
        success: function (response) {
          if (response['status'] == 'success'){
            var result = JSON.parse(response['response']);
            $('#float_value').attr("value",result['amount']);
          }
        else{
            var result = JSON.parse(response['response']);
            $('#float_value').after().text(result['error']);
        }
      }
  
  } )
})
} );

