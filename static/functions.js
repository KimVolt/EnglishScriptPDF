let talkerCount = 0;
let chatHistory = [];

function addTalker() {
    const container = document.getElementById('talker-container');
    talkerCount += 1;

    const talkerInputHTML = `
        <div class="talker-input">
            <input type="text" id="talker${talkerCount}" placeholder="Enter talker name">
            <button onclick="confirmTalker(${talkerCount})">Confirm</button>
        </div>`;
    container.insertAdjacentHTML('beforeend', talkerInputHTML);
}

function confirmTalker(index) {
    const talkerName = document.getElementById(`talker${index}`).value;
    if (talkerName) {
        const messageContainer = document.getElementById('message-container');

        const messageInputHTML = `
            <div class="message-input">
                <h3>${talkerName}</h3>
                <textarea id="message${index}" placeholder="Enter message from ${talkerName}" rows="4"></textarea>
                <button onclick="displayMessage(${index}, '${talkerName}')">Add Message</button>
            </div>`;
        messageContainer.insertAdjacentHTML('beforeend', messageInputHTML);

        document.getElementById(`talker${index}`).disabled = true;
        document.getElementById(`talker${index}`).nextElementSibling.style.display = 'none';
    } else {
        alert('Please enter a Talker name.');
    }
}

function displayMessage(index, talkerName) {
    let message = document.getElementById(`message${index}`).value;

    // 줄바꿈을 HTML의 <br> 태그로 변환
    message = message.replace(/\n/g, '<br>');

    const chatContainer = document.querySelector('#display-container .chat-container');
    
    if (!chatContainer) {
        console.error("chatContainer가 존재하지 않습니다. HTML 구조를 확인하세요.");
        return;
    }

    if (message) {
        const messageHTML = `
            <div class="chat-bubble ${index % 2 === 0 ? 'left' : 'right'}">
                <div class="name">${talkerName}</div>
                <div class="message">${message}</div>
            </div>`;
        
        chatContainer.insertAdjacentHTML('beforeend', messageHTML);
        chatHistory.push({ talker: talkerName, message: message });
        
        document.getElementById(`message${index}`).value = '';
    } else {
        alert('Please enter a message.');
    }
}


function saveAsPDF() {
    const topic = document.getElementById('topic').value;
    const chatContainer = document.querySelector('#display-container .chat-container');

    // 메시지 데이터 수집
    const messages = chatHistory.map(item => ({
        talker: item.talker,
        message: item.message.replace(/\n/g, ' ')  // 줄바꿈을 HTML <br>에서 공백으로 변환
    }));

    fetch('/generate_pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            topic: topic,
            messages: messages 
        })
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "chat_history.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();
    })
    .catch(error => console.error('Error:', error));
}
