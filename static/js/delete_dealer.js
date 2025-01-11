$(function(){
    var dealer_id = $('#car_id').val()
    $('#btn_yes').click({id: dealer_id},function(event){
        var url = "/table/dealers/delete/".concat(event.data.id);

        $.ajax({
            url: url,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            type: 'DELETE',
            success: function(responce){
                alert('Дилер удалён!');
                window.location.replace("/table/dealers");
            },
            error: function(error){
                console.log(error);
            }            
        });
    });

    $('#btn_no').click(function(){
        window.location.replace("/table/dealers")
    })
});