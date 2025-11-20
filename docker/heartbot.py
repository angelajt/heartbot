# pip install google-cloud-dialogflow-cx

import os
import re
from google.cloud.dialogflowcx_v3beta1.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3beta1.types import session

# Set credentials by running `. ./local/.env` in terminal before executing this script

# Set up agent details from environment variables.
PROJECT_ID = os.getenv("PROJECT_ID", "invalid-project-id")
LOCATION_ID = os.getenv("LOCATION_ID", "global")  # or your specific region like "us-central1"

MODULE_TO_AGENT_ID = {
    1: os.getenv("AGENT_ID_MODULE1", "invalid-agent-id-1"),
    2: os.getenv("AGENT_ID_MODULE2", "invalid-agent-id-2"),
    3: os.getenv("AGENT_ID_MODULE3", "invalid-agent-id-3"),
    4: os.getenv("AGENT_ID_MODULE4", "invalid-agent-id-4"),
}

print(f"Loaded agent IDs: {MODULE_TO_AGENT_ID}")

# default agent id if module not found
DEFAULT_AGENT_ID = os.getenv("AGENT_ID_MODULE1", "invalid-agent-id-1")

# Build the agent path.
PATH = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/agents"
LANGUAGE_CODE = "en-us"

# Configure the client with the regional endpoint.
api_endpoint = f"{LOCATION_ID}-dialogflow.googleapis.com:443"
client_options = {"api_endpoint": api_endpoint}
try:
    session_client = SessionsClient(client_options=client_options)
except Exception as e:
    print(f"Error initializing SessionsClient: {e}")

# Send a message to agent. 
# api.py calls this
def chat_with_module(message_text: str, session_id: str, module: int) -> dict:
    agent_id = MODULE_TO_AGENT_ID.get(module, DEFAULT_AGENT_ID)
    # Build the session path using the provided session_id.
    session_path = f"{PATH}/{agent_id}/sessions/{session_id}"

    print(f"Session path: {session_path}")

    text_input = session.TextInput(text=message_text)
    query_input = session.QueryInput(text=text_input, language_code=LANGUAGE_CODE)
    request = session.DetectIntentRequest(
        session=session_path,
        query_input=query_input
    )

    response = session_client.detect_intent(request=request)

    print(response)

    # Extract the response text.
    response_messages = [
        " ".join(msg.text.text) for msg in response.query_result.response_messages
    ]
    agent_text = " ".join(response_messages)

    if not agent_text.strip():
        agent_text = "I'm sorry, I didn't understand that. Could you please rephrase? If this is an emergency, please call 911 immediately."

    # Search for an image tag in the format "[image: <image_url>]"
    image_url = None
    img_match = re.search(r'\[image:\s*(.*?)\]', agent_text)
    if img_match:
        image_url = img_match.group(1).strip()

    # Search for an end tag in the format "[end]"
    end_conversation = False
    end_match = re.search(r'\[end\]', agent_text)
    if end_match:
        agent_text = agent_text[:end_match.start()].strip()
        end_conversation = True

    return {"response": agent_text, "image": image_url, "end": end_conversation}
