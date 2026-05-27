from pydantic import BaseModel
from openai import (
    OpenAI, 
    AuthenticationError, 
    APITimeoutError, 
    APIConnectionError
)

class ExtractedFile(BaseModel):
    id_number: int | None
    name: str
    doc_number: str
    email: str
    location: str
    area: str
    company: str

def parse_text_with_llm(raw_text: str) -> ExtractedFile:
    print("[*] Sending payload to OpenAI daemon...")
    client = OpenAI()

    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Extract document information into the structured schema. Return null for missing fields if allowed."},
                {"role": "user", "content": raw_text}
            ],
            response_format=ExtractedFile
        )
        return completion.choices[0].message.parsed

    except AuthenticationError:
        print("[!] Auth Error: Invalid OpenAI API key.")
        return None
    except (APITimeoutError, APIConnectionError) as e:
        print(f"[!] Network Error: Failed to connect to OpenAI API. Details: {e}")
        return None
    except Exception as e:
        print(f"[!] LLM Parsing Error: {e}")
        return None
