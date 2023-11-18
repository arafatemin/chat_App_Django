// room ismini almak icin
const roomName = JSON.parse(document.getElementById('room-name').textContent);
const conversation = document.getElementById('conversation');
const inputField = document.getElementById('comment');
const sendButton = document.getElementById('send');
const user = JSON.parse(document.getElementById('user').textContent);
const inputFile = document.getElementById('hiddenInput');
inputFile.addEventListener('change', handleFileSelect, false);

function handleFileSelect(e) {
    var file = inputFile.files[0];
    console.log(file);
    getBase64(file);
}

function getBase64(file) {
    var reader = new FileReader(); // dosyamizi okuyor
    reader.readAsDataURL(file);
    reader.onload = function () {


        // Veri URL'sini kullanabilirsiniz (örneğin, bir resim etiketinde gösterme)
        // const imageElement = document.getElementById('image'); // Bir img elementinin ID'sini ayarlayın
        // imageElement.src = reader.result;

        chatSocket.send(JSON.stringify({
            'what_is_it': "image",
            'message': reader.result
        }));


    };


}

// websocket ten bir obje olusturduk o objeye bir baglanti atadik. connection  consumer.connect()
const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + roomName + '/');


// websocketten veri geldiginde calisir or: merhaba.     consumer.chat_message()
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const message_type = data.what_is_it;
    if (message_type === "text") {
        var message = data.message
    } else if (message_type === "image") {
        var message = `<img src="${data.message}" width="400" height="400" />`
    }

    console.log(data.user);
    if (user === data.user) {
        var message = `          
          <div class="row message-body" style="margin-top: 1rem">
            <div class="col-sm-12 message-main-sender">
              <div class="sender">
                 <div class="message-text">
                      ${message}
                     </div>
                        <span class="message-time pull-right">
                           ${data.created_date}
                        </span>
                     </div>
                 </div>
              </div>
            </div>
          </div>`
    } else {
        var message = `          
          <div class="row message-body" style="margin-top: 1rem">
            <div class="col-sm-12 message-main-receiver">
              <div class="receiver">
                 <div class="message-text">
                      ${message}
                     </div>
                        <span class="message-time pull-right">
                           ${data.created_date}
                        </span>
                     </div>
                 </div>
              </div>
            </div>
          </div>`
    }


    conversation.innerHTML += message
    //document.querySelector('#chat-log').value += (data.message + '\n');
    conversation.scrollTop = conversation.scrollHeight
};


// Web socket basglantisi kapandi.   consumer.disconnect()
chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};


// input kismina odaklan
inputField.focus();


// Enter tusunu dinle
inputField.onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        sendButton.click();
    }
};


// input alanindaki mesaji al chatsockete gonder ve input alanini bosalt  consumer.recieve()
sendButton.onclick = function (e) {
    const message = inputField.value
    chatSocket.send(JSON.stringify({
        'what_is_it': "text",
        'message': message
    }));
    inputField.value = ''
};
