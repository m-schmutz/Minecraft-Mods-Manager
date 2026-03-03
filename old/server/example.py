import requests

url = "http://localhost:5000/api/client-check"

payload = {
    "aether-1.21.1-1.5.10-neoforge.jar": "b19386301560a017a458e9790a7b59999e270f93010def0b61e7cbe4c8630dbf",
    "alexsmobs-1.22.16.jar": "05406e48a8cadbc92c331f74f5e047705e76626104e8bfea45f2fd29c05b6888"
}

response = requests.post(url, json=payload)

print("Status:", response.status_code)
print("Response:", response.json())
