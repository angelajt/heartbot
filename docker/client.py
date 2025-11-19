from fastapi.responses import HTMLResponse

def get_client_ui():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Heartbot</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            #chatHistory { width: 100%; height: 300px; border: 1px solid #ccc; padding: 10px; overflow-y: scroll; margin-bottom: 10px; }
            #message_input { width: calc(100% - 100px); padding: 10px; }
            #menu { margin-bottom: 10px; }
            input[type="text"] { padding: 5px; }
            button { padding: 5px 10px; }
        </style>
    </head>
    <body>
        <h2>Heartbot</h2>
        <p>NOTE: This is a proof-of-concept interface, for testing purposes only.</p>
        <h3>Instructions:</h3>
        <p>1. <b>Enter your session ID.</b> The session ID can be any string of numbers and/or letters. This is just so that the bot can keep track of a single conversation (so if you change the session ID, you start a new conversation. You can also go back to an old conversation if you remember the session ID. If you happen to input the same session ID as someone else, you might see some strange behavior because you're basically continuing someone else's chat history).</p>
        <p>2. Select the module in the pull-down menu, starting with Module 1. <b>Please complete all four modules in sequential order.</b></p>
        <p>3. Type your message in the text box and hit Enter or click the Send button. <b>To start, simply send a greeting like "hi" or "hello".</b></p>
        <div>
            <label for="session_id">User Code (Session ID): </label>
            <input type="text" id="session_id" placeholder="Enter your session id">
        </div>
        <div id="menu">
            <label for="module_select">Select Module:</label>
            <select id="module_select">
                <option value="1">Module 1</option>
                <option value="2">Module 2</option>
                <option value="3">Module 3</option>
                <option value="4">Module 4</option>
            </select>
        </div>
        <div id="chatHistory"></div>
        <div>
            <input type="text" id="message_input" placeholder="Type a message">
            <button onclick="sendMessage()">Send</button>
        </div>

        <script>
            // Function to get cookie by name
            function getCookie(name) {
                let cookieArr = document.cookie.split(";");
                for(let i = 0; i < cookieArr.length; i++) {
                    let cookiePair = cookieArr[i].split("=");
                    if(name == cookiePair[0].trim()) {
                        return decodeURIComponent(cookiePair[1]);
                    }
                }
                return null;
            }

            // Function to set cookie
            function setCookie(name, value, days) {
                let expires = "";
                if (days) {
                    let date = new Date();
                    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
                    expires = "; expires=" + date.toUTCString();
                }
                document.cookie = name + "=" + (value || "") + expires + "; path=/";
            }
            
            // On page load, populate session_id from cookie if available
            window.onload = function() {
                let sessionId = getCookie("session_id");
                if(sessionId) {
                    document.getElementById("session_id").value = sessionId;
                }
            };

            // Save session_id to cookie when changed
            document.getElementById("session_id").addEventListener("change", function() {
                setCookie("session_id", this.value, 30);
            });

            // Clear chat history when the module selection is changed.
            document.getElementById("module_select").addEventListener("change", function() {
                document.getElementById("chatHistory").innerHTML = "";
            });

            // Function to format message by inserting a paragraph break for newlines.
            // When a newline is detected in the response, each line becomes its own paragraph.
            // Also add hyperlinks where applicable.
            function formatMessage(sender, message) {
            
                // Remove the image tag from the message text.
                message = message.replace(/\\[image:\\s*.*?\\]/g, "").trim();

                // If the message contains URLs, convert them to clickable links.
                const urlRegex = /(https?:\/\/[^\s]+)/g;
                message = message.replace(urlRegex, function(url) {
                    return '<a href="' + url + '" target="_blank">' + url + '</a>';
                });
                const lines = message.split('\\n');
                let formatted = "<p><strong>" + sender + ":</strong> " + lines[0] + "</p>";
                for (let i = 1; i < lines.length; i++) {
                    formatted += "<p>" + lines[i] + "</p>";
                }
                return formatted;
            }

            async function sendMessage() {
                const session_id = document.getElementById("session_id").value;
                const module = parseInt(document.getElementById("module_select").value);
                const message = document.getElementById("message_input").value;

                if (!session_id) {
                    alert("Please enter your session id!");
                    return;
                }

                // If message is blank or contains only whitespace, do nothing.
                if (!message || message.trim() === "") {
                    return;
                }

                // Append user's message to chat history
                const chatHistory = document.getElementById("chatHistory");
                chatHistory.innerHTML += formatMessage("You", message);

                // Prepare the payload for POST request
                const payload = {
                    module: module,
                    session_id: session_id,
                    message: message
                };

                try {
                    const response = await fetch("/chat", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify(payload)
                    });
                    const data = await response.json();
                    // Append image (if applicable) and bot's response to chat history, inserting paragraph breaks for newlines.
                    if (data.image && data.image.trim() !== "") {
                        chatHistory.innerHTML += `<img src="${data.image}" alt="Image" style="max-width: 100%; margin-bottom: 10px;">`;
                    }
                    chatHistory.innerHTML += formatMessage("Bot", data.response);
                } catch (error) {
                    chatHistory.innerHTML += "<p><strong>Error:</strong> " + error + "</p>";
                }

                // Clear the message input box
                document.getElementById("message_input").value = "";
                // Scroll to the bottom of the chat history
                chatHistory.scrollTop = chatHistory.scrollHeight;
            }

            // Send the message when the user hits Enter, unless the message is blank or whitespace.
            document.getElementById("message_input").addEventListener("keypress", function(event) {
                if (event.key === "Enter") {
                    // Prevent the default action of the Enter key.
                    event.preventDefault();
                    const message = this.value;
                    if (message && message.trim() !== "") {
                        sendMessage();
                    }
                }
            });

        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

