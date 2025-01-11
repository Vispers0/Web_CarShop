$(function(){
    var car_id = $('#car_id').val()
    $('#submit_btn').click({id: car_id},function(event){
        var field = $('#field').find(":selected").val();
        var value = $('#val').val();
        var url = "/table/cars/put/".concat(event.data.id);

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
                alert('Автомобиль изменён!');
                window.location.replace("/table/cars");
            },
            error: function(error){
                console.log(error);
            }            
        });
    });
});