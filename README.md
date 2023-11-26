# OpenAI_Privacy

This repository contains code to create a microservice that extracts PIIs from messages and generates a safe message
with protected PIIs.

Note: This code uses ChatGPT4 APIs.

## Prerequisites

* You will need to have an OpenAI API account, with available usage tokens for ChatGPT4.
* You will also need an API Key, which you can create from https://platform.openai.com/account/api-keys
* Python 3.11 with libraries FastAPI, Pydantic (see requirements.txt)

## Steps to Run Microservice

1. Install the required libraries.
   ```
   pip install -r requirements.txt
   ```
2. Export your OpenAI keys as environment variables.
   ```
   export OPENAI_API_KEY=xxxx
   export OPENAI_API_KEY=yyyy
   ``` 
3. Generate your self-signed certificates.
   ```
   openssl req -x509 -newkey rsa:4096 -nodes -out geraldyong-cert.pem -keyout geraldyong-priv.pem -days 365
   ```
   For example, I'm using mydomain.com as my CN.
   If you change the file names, you will have to change the filenames in `Dockerfile` and in the `privacy_ms.py` file.
4. Edit `/etc/hosts`:
   `vim /etc/hosts`
   Add an entry for your domain.
   ```
   127.0.0.1   localhost mydomain.com
   ```
5. Start up the microservice.
   ```
   uvicorn privacy_ms:app --reload --ssl-certfile certs/geraldyong-cert.pem --ssl-keyfile certs/geraldyong-priv.pem 
   ```
6. Load up the browser to point to your domain, e.g. `https://mydomain.com:8000`
7. Access the `/docs` endpoint.


## Steps to Package As Docker Image

1. Build the docker image.
   ```
   docker build -t singlish:latest .
   ```
2. Bring up the docker serivce.
   ```
   docker compose up -d
   ```
3. Check that the container is up.
   ```
   docker ps -a | grep singlish
   ```

## Example prompt inputs
A list of example prompt inputs can be found in `prompt_chats_list.txt`.