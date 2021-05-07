var recipient;

function loadMessages() {
    $.ajax({
        url: `/get_messages/${recipient}/`,
        method: 'GET',
        success: function(response) {
            $(".chat-panel").html(response)
        },
        complete: function() {
            $(".chat-panel").scrollTop($(".chat-panel")[0].scrollHeight);
        }
    });
}

$(document).ready(function () {
    // var timer
    $(".list-group-item").on("click", function(){
        // clearTimeout(timer)
        $(".list-group-item").removeClass('selected')
        $(this).addClass('selected')

        recipient = $(this).find("span").text()
        loadMessages()
        // timer = setInterval(loadMessages, 3000)
    });

    $("form").submit(function(event){
        var formData = {
            message: $("#message").val()
        }
        $("#message").val("")
        $.ajax({
            url: `/send_message/${recipient}/`,
            method: 'POST',
            data: formData,
            dataType: "json",
        });


        loadMessages();
        event.preventDefault();
    })
})