from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated pre-registered node IDs
registered_nodes = {"NODE-001", "NODE-002"}

@app.route('/connect', methods=['POST'])
def connect_node():
    data = request.get_json()
    node_id = data.get("node_id")

    if node_id in registered_nodes:
        return jsonify({"status": "Access Granted ✅", "node_id": node_id}), 200
    else:
        return jsonify({"status": "Access Denied ❌", "node_id": node_id}), 403

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)