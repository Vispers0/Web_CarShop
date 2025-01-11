$(function(){
    var dealer_id = $('#car_id').val()
    $('#submit_btn').click({id: dealer_id},function(event){
        var field = $('#field').find(":selected").val();
        var value = $('#val').val();
        var url = "/table/dealers/put/".concat(event.data.id);

        $.ajax({
            url: url,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data: JSON.stringify({
                "field": field,
                "value": value
            }),
            type: 'PUT',
            success: function(responce){
                alert('Дилер изменён!');
                window.location.replace("/table/dealers");
            },
            error: function(error){
                console.log(error);
            }            
        });
    });
});