const joinButton = document.getElementById("joinButton");
const createButton = document.getElementById("createButton");
const chatCodeInput = document.getElementById("chatCodeInput");
const chatUI = document.getElementById("chat-ui");
const messageInput = document.getElementById("messageInput");
const messagesDiv = document.getElementById("messages");
const sendButton = document.getElementById("sendButton");
const instructions = document.getElementById("instructions");

let chatCode = '';

// Join chat functionality
joinButton.addEventListener("click", () => {
    const code = chatCodeInput.value.trim();
    if (code) {
        fetch(`/join_chat?code=${code}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    chatCode = code;
                    loadMessages();
                    chatUI.style.display = 'block';
                } else {
                    alert(data.message);
                }
            });
    }
});

// Create chat functionality
createButton.addEventListener("click", () => {
    const code = chatCodeInput.value.trim();
    if (code) {
        fetch(`/create_chat?code=${code}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    chatCode = code;
                    loadMessages();
                    chatUI.style.display = 'block';
                } else {
                    alert(data.message);
                }
            });
    }
});

// Send message
sendButton.addEventListener("click", () => {
    const message = messageInput.value.trim();
    if (message) {
        fetch("/send_message", {
            method: "POST",
            body: new URLSearchParams({ message, code: chatCode }),
            headers: { "Content-Type": "application/x-www-form-urlencoded" }
        })
        .then(response => {
            messageInput.value = '';
            loadMessages();  // Reload messages after sending
        });
    }
});

// Load messages
function loadMessages() {
    fetch(`/get_messages?code=${chatCode}`)
        .then(response => response.json())
        .then(data => {
            messagesDiv.innerHTML = "";  // Clear previous messages
            data.messages.forEach(msg => {
                const messageDiv = document.createElement("div");
                messageDiv.textContent = msg;
                messagesDiv.appendChild(messageDiv);
            });
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        });
}

// Load messages every 1 second (polling for new messages)
setInterval(loadMessages, 1000);

// Space key press to notify about running the server
document.addEventListener("keydown", function(event) {
    if (event.key === " " || event.code === "Space") {
        alert("You need to run the Python server manually! Use 'python app.py' in the terminal.");
    }
});
