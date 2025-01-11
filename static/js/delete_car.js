$(function(){
    var car_id = $('#car_id').val()
    $('#btn_yes').click({id: car_id},function(event){
        var url = "/table/cars/delete/".concat(event.data.id);

        $.ajax({
            url: url,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            type: 'DELETE',
            success: function(responce){
                alert('Автомобиль удалён!');
                window.location.replace("/table/cars");
            },
            error: function(error){
                console.log(error);
            }            
        });
    });

    $('#btn_no').click(function(){
        window.location.replace("/table/cars")
    })
});