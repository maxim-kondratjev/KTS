$(document).ready(function() {
    //$(".chat").scrollTop($(".chat")[0].scrollHeight);
    var form = $(".input");
    form.on('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: '/chat/message_create/',
            data: formData,
            processData: false,
            contentType: false,

            success: (result) => {
                $('.chat').prepend(result['rendered_template']);
                $('#message_input').val("");
               // $(".chat").animate({ scrollTop: $(".chat")[0].scrollHeight}, 800);
            }
        });
    });

    setInterval(function () {
        const lastId = $('.message').first().data("id");

            $.ajax({
            type: 'GET',
            url: '/chat/messages/',
            data: {'last_id': lastId},


            success: (result) => {
                if (result !== ""){
                    $('.chat').prepend(result);
                   // $(".chat").animate({ scrollTop: $(".chat")[0].scrollHeight}, 800);
                }
            }
        });

    }, 2*1000);
});
