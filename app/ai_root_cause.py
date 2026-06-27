import os
import requests

API_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "model": "meta-llama/Llama-3.1-8B-Instruct",
    "messages": [
        {
            "role": "user",
            "content": "Explain why running Flask with debug=True is dangerous."
        }
    ],
    "max_tokens": 300
}

response = requests.post(API_URL, headers=headers, json=payload)

print(response.status_code)
print(response.text)