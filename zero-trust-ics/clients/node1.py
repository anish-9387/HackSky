import sys
import os
import hashlib
import requests
import json

# Add the GATEWAY directory to sys.path
current_dir = os.path.dirname(__file__)
gateway_path = os.path.abspath(os.path.join(current_dir, '..', 'gateway'))
sys.path.insert(0, gateway_path)

from db import get_private_key
from pqc_sim import encrypt_session_key

node_id = "NODE-001"

# Load private key from DB
private_key = get_private_key(node_id)
if not private_key:
    raise Exception("Node not registered. Run setup_node.py first.")

# Derive public key
public_key = hashlib.sha256(private_key.encode()).hexdigest()
session_key, cipher = encrypt_session_key(public_key)

# Send request to gateway
payload = {
    "node_id": node_id,
    "session_key": session_key,
    "cipher": cipher
}

gateway_url = "http://127.0.0.1:5000/connect"
response = requests.post(gateway_url, json=payload)
print("Client Response:", response.status_code, response.json())