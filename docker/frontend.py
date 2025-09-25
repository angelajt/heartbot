from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import backend  # Import the backend module to talk to the Google conversational agents API

app = FastAPI()

# Simple root endpoint.
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Example endpoint similar to the one in x/fastapi/example/main.py.
@app.get("/items/{item_id}/{name}")
def read_item(item_id: int, q: Optional[str] = None, r: Optional[str] = None, name: str = "default_name"):
    return {"item_id": item_id, "name": name, "q": q, "r": r}

# Define request and response models for the /chat endpoint.
class ChatRequest(BaseModel):
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
        agent_response = backend.chat_with_agent(chat.message, chat.session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return ChatResponse(response=agent_response)
