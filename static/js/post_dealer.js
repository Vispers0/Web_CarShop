$(function(){
    $('#submit_btn').click(function(){
        $.ajax({
            url: '/table/dealers/post',
            data: $('form').serialize(),
            type: 'POST',
            success: function(responce){
                alert('Дилер добавлен!');
                window.location.replace("/table/dealers");
            },
            error: function(error){
                console.log(error);
            }            
        });
    });
});