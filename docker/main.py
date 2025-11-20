import uvicorn
from api import app

# Set credentials by running `. ./local/.env` in terminal before executing this script

if __name__ == "__main__":
    # Start the FastAPI frontend API server on host 0.0.0.0 and port 8042.
    uvicorn.run(app, host="0.0.0.0", port=8042, log_level="info")
