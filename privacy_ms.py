# Models and Types
from typing import List
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI, HTTPException

# SSL
import ssl

# ---------------------------------------------------------------

# Load Helper Functions
import helper

# Set up the Server
app = FastAPI()
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('certs/geraldyong-cert.pem', keyfile='certs/geraldyong-priv.pem')


# Define the base models
class ClearText(BaseModel):
    msg: str

class ClearTextList(BaseModel):
    msg_list: List[ClearText]

class SafeText(BaseModel):
    msg: str

class SafeTextList(BaseModel):
    msg_list: List[SafeText]


@app.get("/")
async def get_root():
    return {"version": "0.0.1"}


@app.post("/deidentify/msg")
async def deidentify_text(clearmsg: ClearText):
    # Deidentifies text.
    try:
        prompt = f"""
        I will provide a JSON enclosed in triple backticks. The JSON contains a sample text.

        For this text, please perform the following:
        1. Identify the category of personal identifiers and quasi identifiers in the text
        2. Determine if the identifier type is personal or quasi.
        3. Apply an appropriate privacy enhancing technique on the identifier:
        a.  For names, please generate a random full name. Do not use a placeholder.
        b. For NRICs, keep only the last 4 characters.
        c. For date of birth, replace with age, rounded up to the nearest decade.
        d. For addresses, block out the block number and unit numbers with '0'.
        e. For postal codes, replace the last 3 characters with '000'.
        f. For phone numbers, keep the first digit and replace the rest of the the digits with numbers.
        g. For emails, replace the front part with a random string of alphanumeric characters. Do not use a placeholder.

        Do not explain your processing.
        Return only a JSON containing the sample text with the identifiers replaced with their masked values.

        JSON:
        ```
        {clearmsg}
        ```
        """

        safemsg_out = helper.deidentify_text(prompt, max_tokens = 2000, llm_model = "gpt-4-1106-preview")
        safemsg = SafeText(safemsg_out)
        
        return safemsg
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.post("/deidentify/msg/pii")
async def deidentify_get_pii(clearmsg: ClearText):
    # Extracts the list of PII from text.
    #try:
        prompt = f"""
        I will provide a JSON enclosed in triple backticks. The JSON contains a sample text.

        For this text, please perform the following:
        1. Identify the category of personal identifiers and quasi identifiers in the text
        2. Determine if the identifier type is personal or quasi.
        3. Apply an appropriate privacy enhancing technique on the identifier:
        a.  For names, please generate a random full name. Do not use a placeholder.
        b. For NRICs, keep only the last 4 characters.
        c. For date of birth, replace with age, rounded up to the nearest decade.
        d. For addresses, block out the block number and unit numbers with '0'.
        e. For postal codes, replace the last 3 characters with '000'.
        f. For phone numbers, keep the first digit and replace the rest of the the digits with numbers.
        g. For emails, replace the front part with a random string of alphanumeric characters. Do not use a placeholder.

        Do not explain your processing.
        Return only a JSON with the following keys 'msg' containing a list of keys 'pii_category','pii_type',
        'original_value','masked_value'.

        JSON:
        ```
        {clearmsg}
        ```
        """
        safemsg = helper.deidentify_text(prompt, max_tokens = 2000, llm_model = "gpt-4-1106-preview")

        return safemsg
    #except Exception as e:
    #    raise HTTPException(status_code=400, detail=str(e))


@app.post("/deidentify/msg_list")
async def deidentify_list(clearmsglist: ClearTextList):
    # Deidentifies a list of text.
    try:
    # Create ab empty list to store the converted quotes.
        prompt = f"""
        I will provide a JSON list of sample text enclosed in triple backticks.

        For each text in the list, please perform the following:
        1. Identify the category of personal identifiers and quasi identifiers in the text
        2. Determine if the identifier type is personal or quasi.
        3. Apply an appropriate privacy enhancing technique on the identifier:
        a. For names, please generate a random full name. Do not use a placeholder.
        b. For NRICs, keep only the last 4 characters.
        c. For date of birth, replace with age, rounded up to the nearest decade.
        d. For addresses, block out the block number and unit numbers with '0'.
        e. For postal codes, replace the last 3 characters with '000'.
        f. For phone numbers, keep the first digit and replace the rest of the the digits with numbers.
        g. For emails, replace the front part with a random string of alphanumeric characters. Do not use a placeholder.

        Do not explain your processing.
        Return only a JSON with the following key 'msg_list' containing a list of 'msg' keys, each 'msg' key is the transformed
        sample text with the identifiers replaced with their masked values.

        Sample text:
        ```
        {clearmsglist}
        ```
        """
        safemsglist_out = helper.deidentify_text(prompt, max_tokens = 2000, llm_model = "gpt-4-1106-preview")
        safemsglist = SafeTextList(**safemsglist_out)

        return safemsglist
    except Exception as e:
        # Handle exceptions
        raise HTTPException(status_code=500, detail=str(e))