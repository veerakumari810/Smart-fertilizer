import requests
import json

url = "http://localhost:8000/chat"
payload = {
    "query": "What is the best fertilizer for rice?"
}

try:
    response = requests.post(url, json=payload)
    print(response.status_code)
    print(response.json())
except Exception as e:
    print(f"Error: {e}")
