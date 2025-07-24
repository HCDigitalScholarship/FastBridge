document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const chatInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    let chatHistory = [];
    function generateUUID() {
    if (window.crypto && crypto.randomUUID) {
        return crypto.randomUUID();
    }

    // Fallback UUID v4 generator (RFC4122 compliant)
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        const r = (Math.random() * 16) | 0;
        const v = c === 'x' ? r : (r & 0x3) | 0x8;
        return v.toString(16);
    });
    }

    const chatId = generateUUID(); 


    async function sendMessage(message, initial = false) {
        appendMessage("user", message);
        chatInput.value = "";

        const loading = document.getElementById("loading");
        loading.style.display = "block"; 
        chatBox.scrollTop = chatBox.scrollHeight;

        try {
            const res = await fetch("/stats/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message,
                history: chatHistory,
                chat_id: chatId,
                initial,
                ...(initial ? { context } : {}), // send context only for initial message
            }),
            });

            const data = await res.json();
            const response = data.response;

            appendMessage("bot", response);
            chatHistory.push({ role: "user", parts: message });
            chatHistory.push({ role: "model", parts: response });
        } catch (err) {
            console.error("Error:", err);
            appendMessage("bot", "Something went wrong.");
        } finally {
            loading.style.display = "none"; // hide it
        }
    }

    async function appendMessage(role, content) {
        const messageDiv = document.createElement("div");
        messageDiv.className = role === "user" ? "user-msg" : "bot-msg";
        chatBox.appendChild(messageDiv);
        chatBox.appendChild(document.getElementById("loading")); // keep loading at bottom

        const prefix = `<span class="${role}">${role === "user" ? "You" : "Bot"}:</span> `;
        const htmlBody = marked.parse(content);

        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = htmlBody;
        const plainText = tempDiv.innerText || tempDiv.textContent;

        let i = 0;
        const typingInterval = 10;
        messageDiv.innerHTML = prefix;

        const typeChar = () => {
        if (i < plainText.length) {
            messageDiv.innerHTML = prefix + plainText.slice(0, i + 1);
            chatBox.scrollTop = chatBox.scrollHeight;
            i++;
            setTimeout(typeChar, typingInterval);
        } else {
            messageDiv.innerHTML = prefix + htmlBody;
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        };

        typeChar();
    }

    sendButton.addEventListener("click", () => {
        const message = chatInput.value.trim();
        if (message !== "") sendMessage(message);
    });

    chatInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            sendButton.click();
        }
    });

    // Auto-send an initial message
    sendMessage("What are the key insights from the statistical analysis of this text?", true);
});

document.addEventListener("DOMContentLoaded", function () {
    const chatTab = document.getElementById("chatSlideOutTab");
    const chatSlideOut = document.getElementById("chatSlideOut");

    chatTab.addEventListener("click", () => {
        chatSlideOut.classList.toggle("showChatSlideOut");
    });
});
