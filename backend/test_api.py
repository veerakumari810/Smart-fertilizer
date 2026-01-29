import requests
import json

url = "http://localhost:8000/predict"
payload = {
    "Soil_N": 45,
    "Soil_P": 20,
    "Soil_K": 60,
    "Soil_pH": 6.5,
    "Soil_Moisture": 30,
    "Crop_Name": "Rice",
    "Season": "Kharif"
}

try:
    response = requests.post(url, json=payload)
    print(response.status_code)
    print(response.json())
except Exception as e:
    print(f"Error: {e}")
