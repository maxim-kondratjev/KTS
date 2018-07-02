function resetFormElement(e) {
  e.wrap('<form>').closest('form').get(0).reset();
  e.unwrap();

  // Prevent form submission
  e.stopPropagation();
  e.preventDefault();
}

$(document).ready(function () {
    var form = $(".input");

    $('#button_attach').change(function() {
        var file = $('#button_attach')[0].files[0];
        $(".attached_file_span").text("Выбран файл: " + file.name);
        $(".attached_file").css('display', 'block');
        $(".chat").css('height', 'calc(100% - 60px - 70px - 20px)');
    });

    form.on('submit', function (e) {
        e.preventDefault();
        $(".attached_file").css('display', 'none');
        $(".chat").css('height', 'calc(100% - 60px - 60px)');

        const formData = new FormData(this);

        if ($("#button_attach")[0].files[0] != undefined || $("#message_input").val() != "") {
            $.ajax({
                type: 'POST',
                url: '/chat/message_create/',
                data: formData,
                processData: false,
                contentType: false,

                success: (result) => {
                    $('.chat').prepend(result['rendered_template']);
                    $('#message_input').val("");
                    resetFormElement($("#button_attach"))
                }
            });
        }
    });


    setInterval(function () {
        var lastId = $('.message').first().data("id");
        if (lastId == null){
            lastId = 0;
        }
        $.ajax({
            type: 'GET',
            url: '/chat/messages/',
            data: {'last_id': lastId},

            success: (result) => {
                if (result.toString().indexOf('<title>') + 1) {
                    window.location.replace('../chat/login');
                }
                else if (result !== "") {
                    $('.chat').prepend(result);
                }
            }
        });

    }, 2 * 1000);
});
