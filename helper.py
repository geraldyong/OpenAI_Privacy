import os
from openai import OpenAI
import re

# ---------------------------------------------------------------

# Helper functions to post-process returned results
def strip_pretext(msg: str) -> str:
    # Find the position of '{'
    pos = msg.find('{')

    # If '{' is found in the string
    if pos != -1:
        # Slice the string from the position of '{' to the end
        result = msg[pos:]
    else:
        # If '{' is not found in the string
        result = msg

    return result

def escape_single_quotes(s: str) -> str:
    # Replace single quotes that are not preceded by a backslash with escaped single quotes
    return re.sub(r"(?<!\\)'", r"\'", s)

def remove_extra_spaces(s: str) -> str:
    # Remove extra spaces
    return re.sub(r"\s+", r" ", s)

def remove_triple_backticks(s: str) -> str:
    # Remove triple backticks
    return re.sub(r"```", r"", s)

def check_starting_brace(s: str) -> str:
    # Check that there is a starting brace
    return s if s.startswith('{') else '{' + s

def check_ending_brace(s: str) -> str:
    # Check that there is an ending brace
    return s if s.endswith('}') else s + '}'

def remove_json_prefix(s: str) -> str:
    # Remove a JSON prefix.
    return re.sub(r"^JSON", r"", s, flags=re.IGNORECASE)


# OpenAI
client = OpenAI(
  api_key = os.getenv('OPENAI_API_KEY'),
)

def deidentify_text(prompt, max_tokens, llm_model = "gpt-4-1106-preview"):
    # Takes a prompt that contains a message and deidentifies it.
    response = client.chat.completions.create(
        model = llm_model,
        max_tokens = max_tokens,
        messages = [
            {"role": "system", "content": prompt},
        ]
    )

    return eval(
                remove_json_prefix(
                    remove_triple_backticks(
                        response.choices[0].message.content.strip()
                    )
                )
            )
        