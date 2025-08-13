let chatInitialized = false;
let chatHistory = [];
let chatId = null;
let loadedTexts = new Set(); 
let allTextContexts = {}; 
let expectedTextCount = 0; 
let hasAcknowledgedAllTexts = false; 

function generateUUID() {
    if (window.crypto && crypto.randomUUID) {
        return crypto.randomUUID();
    }

    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        const r = (Math.random() * 16) | 0;
        const v = c === 'x' ? r : (r & 0x3) | 0x8;
        return v.toString(16);
    });
}

async function initializeChat(firstTextContext) {
    if (chatInitialized) return;
    
    chatId = generateUUID();
    chatInitialized = true;
    
    const currentUrl = window.location.pathname;
    const urlMatch = currentUrl.match(/\/Compare\/result\/([^\/]+)/);
    if (urlMatch) {
        const textsPart = urlMatch[1];
        const textsArray = textsPart.split('+').filter(text => text.trim() !== '');
        expectedTextCount = textsArray.length;
    } else {
        expectedTextCount = 1;
    }
    
    const chatBox = document.getElementById("chat-box");
    const chatInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const chatForm = document.getElementById("chat-form");

    if (!chatBox || !chatInput || !sendButton) {
        console.error("Chat elements not found");
        return;
    }

    const textKey = `${firstTextContext.text_name}_${firstTextContext.start_section}_${firstTextContext.end_section}`;
    loadedTexts.add(textKey);
    allTextContexts[textKey] = firstTextContext;

    appendMessage("system", ` Loading text: **${firstTextContext.text_name}** (${firstTextContext.start_section}-${firstTextContext.end_section})...`);

    chatForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (message !== "") sendMessage(message);
    });

    sendButton.addEventListener("click", (e) => {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (message !== "") sendMessage(message);
    });

    chatInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            sendButton.click();
        }
    });
}

async function addTextToChat(textContext) {
    if (!chatInitialized || !chatId) {
        console.error("Chat not initialized");
        return;
    }

    const textKey = `${textContext.text_name}_${textContext.start_section}_${textContext.end_section}`;
    
    // Don't add the same text again
    if (loadedTexts.has(textKey)) {
        return;
    }
    
    loadedTexts.add(textKey);
    allTextContexts[textKey] = textContext;

    // Show system message about new text being loaded
    appendMessage("system", `➕ Loading text: **${textContext.text_name}** (${textContext.start_section}-${textContext.end_section})...`);

    if (loadedTexts.size >= expectedTextCount && !hasAcknowledgedAllTexts) {
        hasAcknowledgedAllTexts = true;
        await sendAllTextsAcknowledgment();
    } 
    else if (hasAcknowledgedAllTexts && loadedTexts.size > expectedTextCount) {
        await sendNewTextAcknowledgment(textContext);
    }
}

async function sendMessage(message, initial = false) {
    appendMessage("user", message);
    const chatInput = document.getElementById("user-input");
    chatInput.value = "";

    const loading = document.getElementById("loading");
    if (loading) {
        loading.style.display = "block"; 
    }
    
    const chatBox = document.getElementById("chat-box");
    if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    try {
        
        const res = await fetch("/stats/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message,
                history: chatHistory,
                chat_id: chatId,
                initial: false,
                mode: "compare",
                all_contexts: allTextContexts 
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
        if (loading) {
            loading.style.display = "none";
        }
    }
}

async function appendMessage(role, content) {
    const chatBox = document.getElementById("chat-box");
    if (!chatBox) return;

    const messageDiv = document.createElement("div");
    messageDiv.className = role === "user" ? "user-msg" : role === "bot" ? "bot-msg" : "system-msg";
    chatBox.appendChild(messageDiv);
    
    const loading = document.getElementById("loading");
    if (loading) {
        chatBox.appendChild(loading);
    }

    let prefix;
    if (role === "system") {
        prefix = `<span class="system">System:</span> `;
    } else {
        prefix = `<span class="${role}">${role === "user" ? "You" : "Bot"}:</span> `;
    }
    
    const htmlBody = marked.parse(content);

    const tempDiv = document.createElement("div");
    tempDiv.innerHTML = htmlBody;
    const plainText = tempDiv.innerText || tempDiv.textContent;

    let i = 0;
    const typingInterval = role === "system" ? 5 : 10;
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

async function sendAllTextsAcknowledgment() {
    try {
        const textNames = Object.values(allTextContexts).map(ctx => 
            `${ctx.text_name} (${ctx.start_section}-${ctx.end_section})`
        );
        
        let acknowledgmentText;
        if (textNames.length === 1) {
            acknowledgmentText = `I have loaded "${textNames[0]}".`;
        } else {
            acknowledgmentText = `I have loaded the following texts:\n\n${textNames.map(name => `- ${name}`).join('\n')}`;
        }

        appendMessage("bot", acknowledgmentText);
        
    } catch (error) {
        console.error("Error sending acknowledgment for all texts:", error);
    }
}

async function sendNewTextAcknowledgment(textContext) {
    try {
        const textName = `${textContext.text_name} (${textContext.start_section}-${textContext.end_section})`;
        const acknowledgmentText = `I have loaded "${textName}".`;

        appendMessage("bot", acknowledgmentText);
        
    } catch (error) {
        console.error("Error sending acknowledgment for new text:", error);
    }
}

window.chatCompare = {
    initializeChat,
    addTextToChat,
    sendMessage
};
