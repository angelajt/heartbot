from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import heartbot  # Import the heartbot library to talk to the Google conversational agents API
from fastapi.responses import HTMLResponse
import client  # Import the client module that provides the UI

app = FastAPI()

# Define request and response models for the /chat endpoint.
class ChatRequest(BaseModel):
    module: int
    session_id: str   # Required session id provided by the client.
    message: str

class ChatResponse(BaseModel):
    response: str
    image: Optional[str] = None
    end: bool

# Endpoint that receives a chat message from phone apps or web apps,
# forwards it to the heartbot library, and returns the agent's response as JSON.
# The response_model defines the response schema.
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(chat: ChatRequest):
    try:
        agent_response = heartbot.chat_with_module(chat.message, chat.session_id, chat.module)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return ChatResponse(**agent_response)

# Route the root URL to serve the client UI.
@app.get("/", response_class=HTMLResponse)
def root():
    return client.get_client_ui()
