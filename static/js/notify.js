
const chatroom_id = JSON.parse(document.getElementById('json-chatroom').textContent)
const logged_in_user = JSON.parse(document.getElementById('json-username').textContent)
const receiver=JSON.parse(document.getElementById('json-receiver_username').textContent)
const notify_socket = new WebSocket("ws://" + window.location.host + "/ws/notify/")


notify_socket.onopen = function(e){
    console.log("CONNECTED TO NOTIFICATION");
    console.log(e);
}

var count_badge = document.getElementById('count_badge')

notify_socket.onmessage = function(e){
    
    print("in notification socket")
    const data = JSON.parse(e.data)
    count_badge.innerHTML = data.count
}

notify_socket.onclose = function(e){
    console.log("DISCONNECTED FROM NOTIFICATION");
}

