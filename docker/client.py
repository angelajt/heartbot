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
                    date.setTime(date.getTime() + (days*24*60*60*1000));
                    expires = "; expires=" + date.toUTCString();
                }
                document.cookie = name + "=" + (value || "")  + expires + "; path=/";
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

            async function sendMessage() {
                const session_id = document.getElementById("session_id").value;
                const module = parseInt(document.getElementById("module_select").value);
                const message = document.getElementById("message_input").value;

                if (!session_id) {
                    alert("Please enter your session id!");
                    return;
                }

                if (!message) {
                    return;
                }

                // Append user's message to chat history
                const chatHistory = document.getElementById("chatHistory");
                chatHistory.innerHTML += "<p><strong>You:</strong> " + message + "</p>";

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
                    // Append bot's response to chat history
                    chatHistory.innerHTML += "<p><strong>Bot:</strong> " + data.response + "</p>";
                } catch (error) {
                    chatHistory.innerHTML += "<p><strong>Error:</strong> " + error + "</p>";
                }

                // Clear the message input box
                document.getElementById("message_input").value = "";
                // Scroll to the bottom of the chat history
                chatHistory.scrollTop = chatHistory.scrollHeight;
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
