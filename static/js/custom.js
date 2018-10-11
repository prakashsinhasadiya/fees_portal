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
  $("#amount_type_4,#amount_type_3,#amount_type_2,#amount_type_1").click(function (event) {
    var value = this.value
    var selected = this.checked
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
            debugger;
            $('#float_value').after().text(result['error']);
        }
      }
  
  } )
})
} );

