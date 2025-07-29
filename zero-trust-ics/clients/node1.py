import requests

gateway_url = "http://127.0.0.1:5000/connect"
payload = {"node_id": "NODE-001"}  # Valid node

response = requests.post(gateway_url, json=payload)

print("Legit Client Response:", response.status_code, response.json())