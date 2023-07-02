const room_id = JSON.parse(document.getElementById('room_id').textContent)
const logged_in_user = JSON.parse(document.getElementById('logged_in_user').textContent)
const friends=JSON.parse(document.getElementById('friend_serializer').textContent)
const receiver_id=JSON.parse(document.getElementById('receiver_id').textContent)
// Create a new WebSocket
const chatSocket = new WebSocket('ws://'+ window.location.host +'/ws/direct/' + room_id + "/");


document.getElementById('send-button').onclick = function(e){
    e.preventDefault();
    console.log("hello world")
    const messageInput = document.getElementById('message-input');
    const chat_message = messageInput.value;
    messageInput.value = ""
    chatSocket.send(JSON.stringify({
        'message_sender': logged_in_user,
        'message_content': chat_message
    }))
}

// Application layer Headers dont work on HTTP
chatSocket.onmessage = function(e){
    data = JSON.parse(e.data)
    var currenttime=new Date()
    let message_content = data.message_content
    let message_sender = data.message_sender
    let html = `<tr>
                    <td>
                        <p class="bg-success float-right chat_message p-2 mt-2 mr-5 shadow-sm text-white rounded ">
                            ${message_content}
                            <small class="ml-2" style="font-size: 12px; color:#8FBEA6;">just now</small>
                        </p>
                    </td>
                </tr> `
    let newhtml =` <tr>
                    <td>
                        <p class="bg-primary float-left chat_message p-2 mt-2 mr-5 shadow-sm text-white rounded ">
                            ${message_content}   
                            <small class="ml-2" style="font-size: 12px; color:#8FBEA6;">just now</small>
                        </p>
                    </td>
                </tr>`


var lasttext=document.getElementsByClassName('friends-dm')
var lastseen=document.getElementsByClassName('time')
lasttext.innerHTML=null
for(let key in friends)
{
    if(friends.hasOwnProperty(key))
    {
        
        if(receiver_id==friends[key].unique_id)
    {
        console.log(friends[key].last_seen)
         friends[key].last_seen=currenttime
         friends[key].last_text=message_content
    }
    }
}

friends.sort(function(a, b) {
    var timeA = new Date(a.last_seen);
    var timeB = new Date(b.last_seen);
    return timeB - timeA;
  });

for(let i in friends)
{
    if(friends.hasOwnProperty(i))
    {
        console.log(friends[i].user.username)
        console.log(friends[i].last_seen)
    var cur=new Date(friends[i].last_seen)
    var img=friends[i].image
    var display_time=cur.getHours()+":"+cur.getMinutes()
    let replace=` <a href="/chat/direct/${friends[i].unique_id}" class="text-dark" onclick="directMessage();" style="cursor: pointer; text-decoration: none;">
    <div class="d-flex w-100 align-items-center justify-content-between mb-3 friends">
        <div class="d-flex justify-content-center align-items-center">
            <img src="${img}" alt="" class="mr-4 profile-image rounded-circle">
            <div class="profile_username">
                ${friends[i].user.username} <br> <small class="dmtext">${ friends[i].last_text }</small>
            </div>
        </div>
        <div class="time"><small>${display_time}</small></div>
    </div>
</a>`
document.getElementById('show_chats').insertAdjacentHTML('beforeend', replace) 
    }
}


    if(logged_in_user == message_sender)
        document.getElementById('displayed_messages').insertAdjacentHTML('beforeend', html) 
    else
        document.getElementById('displayed_messages').insertAdjacentHTML('beforeend', newhtml)

    //scroll();       // whenever we get a new message we will scroll to top
}


/*function scroll(){
    const mcontainer = document.getElementById('chat-container');
    mcontainer.scrollTop = mcontainer.scrollHeight;
}

scroll()*/




//javascript object->json object
//JSON.stringify()
//json object->javascript object
//JSON.parse()

//python object->json obj
//json.dumps()
//json obj->python obj
//json.loads()
