import requests

gateway_url = "http://127.0.0.1:5000/connect"
payload = {
    "node_id": "HACKER-999",
    "session_key": "malicious-session",
    "cipher": "invalidcipher123"
}
response = requests.post(gateway_url, json=payload)
print("Rogue Client Response:", response.status_code, response.json())