$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname.slice(5));
    //var chatsock = new WebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);

    chatsock.onmessage = function(message) {
        var data = JSON.parse(message.data);
        var chat = $("#chat")
        var ele = $('<tr></tr>')

        ele.append(
            $("<td></td>").text(data.timestamp)
        )
        ele.append(
            $("<td></td>").text(data.handle)
        )
        ele.append(
            $("<td></td>").text(data.message)
        )
        
        chat.append(ele)
    };

    $("#chatform").on("submit", function(event) {
        var message = {
            handle: $('#handle').val(),
            message: $('#message').val(),
        }
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();
        return false;
    });

    var apiUrl = 'http://127.0.0.1:8000/api/v1/messages/';
    $.ajax({
        url: apiUrl, 
        dataType: 'json',
        success: function(data) {
            $.each(data, function(index, item) {
                console.log(item.message);
            });
        },
        complete: function(data, textStatus){
            console.log('all loaded!');
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + errmsg + ": "+ xhr.responseText);
        }
    });
});