var recipient;
var isChecked = false

function loadMessages() {
    $.ajax({
        url: `/get_messages/${recipient}/`,
        method: 'GET',
        success: function(response) {
            $(".chat-panel").html(response)
        },
        complete: function() {
            if (isChecked) {
                $(".chat-panel").scrollTop($(".chat-panel")[0].scrollHeight);
                isChecked = false
            }
        }
    });
}

$(document).ready(function () {
    var timer
    $(".list-group-item").on("click", function(){
        isChecked = true
        
        clearTimeout(timer)
        $(".list-group-item").removeClass('selected')
        $(this).addClass('selected')

        recipient = $(this).find("span").text()
        loadMessages()
        timer = setInterval(loadMessages, 3000)

        $(".chat-panel").scrollTop($(".chat-panel")[0].scrollHeight);
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