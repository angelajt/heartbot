FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

# This is to work around PEP 668 issues, which isn't an issue for containers
ENV PIP_BREAK_SYSTEM_PACKAGES=1 

RUN pip3 install fastapi # Web framework for building APIs
RUN pip3 install google-cloud-dialogflow-cx # Dialogflow CX library
RUN pip3 install "uvicorn[standard]" # ASGI server for serving FastAPI applications

WORKDIR /heartbot

COPY . /heartbot/

CMD ["./run.sh"]
