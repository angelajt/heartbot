from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import backend  # Import the backend module to talk to the Google conversational agents API

app = FastAPI()

# Define request and response models for the /chat endpoint.
class ChatRequest(BaseModel):
    module: int
    session_id: str   # Required session id provided by the client.
    message: str

class ChatResponse(BaseModel):
    response: str

# Endpoint that receives a chat message from phone apps or web apps,
# forwards it to the backend module, and returns the agent's response as JSON.
# The response_model defines the response schema.
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(chat: ChatRequest):
    try:
        agent_response = backend.chat_with_module(chat.message, chat.session_id, chat.module)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return ChatResponse(response=agent_response)
