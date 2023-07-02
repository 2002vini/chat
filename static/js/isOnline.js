const socket = new WebSocket("ws://" + window.location.host + "/ws/status/")

socket.onopen = function(e){
    socket.send(JSON.stringify({
        'status': 'online',
    }))
}

window.addEventListener("beforeunload", function(event) {
    socket.send(JSON.stringify({
        'status': "offline",
    }))
});
