const group_id = JSON.parse(document.getElementById('group_id').textContent)
const logged_in_user = JSON.parse(document.getElementById('logged_in_user').textContent)

const group_socket = new WebSocket('ws://'+ window.location.host +'/ws/group/' +  group_id + "/")

document.getElementById('send-button').onclick = function(e){
    e.preventDefault();
    const messageInput = document.getElementById('message-input');
    const message_content = messageInput.value;
    console.log(message_content)

    messageInput.value = ""
    group_socket.send(JSON.stringify({
        'message_sender': logged_in_user,
        'message_content': message_content
    }))
}

group_socket.onmessage = function(e){
    data = JSON.parse(e.data)
    let message_content = data.message_content
    let message_sender = data.message_sender
    let html = `<tr>
                    <td>
                        <p class="d-flex flex-column mr-auto bg-primary float-left chat_message p-2 mt-2 mr-5 shadow-sm text-white rounded ">
                            <small style="font-size: 12px; color:#8FBEA6;">${message_sender}</small>
                            ${message_content}
                            <small style="font-size: 10px; color:#8FBEA6;">11:21 PM</small>
                        </p>
                    </td>
                </tr> `

    let newhtml =` <tr>
                    <td>
                        <p class="d-flex flex-column ml-auto bg-success chat_message p-2 mt-2 mr-5 shadow-sm text-white rounded">
                            <small style="font-size: 12px; color:#8FBEA6;">${message_sender}</small>
                            ${message_content}
                            <small style="font-size: 10px; color:#8FBEA6;">11:21 PM</small>
                        </p>
                    </td>
                </tr>`

    if(logged_in_user == message_sender)
        {document.getElementById('displayed_messages').insertAdjacentHTML('beforeend', newhtml)
        }
    else
        document.getElementById('displayed_messages').insertAdjacentHTML('beforeend', html)

}