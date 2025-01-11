$(function(){
    $('#submit_btn').click(function(){
        $.ajax({
            url: '/table/cars/post',
            data: $('form').serialize(),
            type: 'POST',
            success: function(responce){
                alert('Автомобиль добавлен!');
                window.location.replace("/table/cars");
            },
            error: function(error){
                console.log(error);
            }            
        });
    });
});