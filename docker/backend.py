# pip install google-cloud-dialogflow-cx

import os
from google.cloud.dialogflowcx_v3beta1.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3beta1.types import session

# Set credentials by running `. ./local/.env` in terminal before executing this script

# Set up agent details from environment variables.
PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID", "your-project-id")
LOCATION_ID = os.getenv("DIALOGFLOW_LOCATION_ID", "global")  # or your specific region like "us-central1"
AGENT_ID = os.getenv("DIALOGFLOW_AGENT_ID", "your-agent-uuid")  # The UUID part from the agent name

# Build the agent path.
AGENT = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/agents/{AGENT_ID}"
LANGUAGE_CODE = "en-us"

# Configure the client with the regional endpoint.
api_endpoint = f"{LOCATION_ID}-dialogflow.googleapis.com:443"
client_options = {"api_endpoint": api_endpoint}
session_client = SessionsClient(client_options=client_options)

# Function to send a message to your agent. Frontend should call this.
# Now requires the client to provide a session_id, allowing client-controlled persistent sessions.
def chat_with_agent(message_text: str, session_id: str) -> str:
    # Build the session path using the provided session_id.
    session_path = f"{AGENT}/sessions/{session_id}"
    
    text_input = session.TextInput(text=message_text)
    query_input = session.QueryInput(text=text_input, language_code=LANGUAGE_CODE)
    request = session.DetectIntentRequest(
        session=session_path, 
        query_input=query_input
    )
    
    response = session_client.detect_intent(request=request)
    
    # Extract the response text.
    response_messages = [
        " ".join(msg.text.text) for msg in response.query_result.response_messages
    ]
    return " ".join(response_messages)
