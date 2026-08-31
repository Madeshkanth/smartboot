from flask import Flask, render_template, request, jsonify
from flask_sock import Sock
import json

app = Flask(__name__)
sock = Sock(app)

# Store latest value
latest_data = {
    "average": 0
}

# Connected browser clients
browser_clients = set()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/latest")
def api_latest():
    return jsonify(latest_data)

# ==========================================
# REPLACED: HTTP POST Route for ESP32
# ==========================================
@app.route("/api/boot-data", methods=["POST"])
def receive_boot_data():
    try:
        data = request.get_json()
        
        if data and "average" in data:
            average = float(data["average"])
            latest_data["average"] = average
            print(f"Received Average: {average}")

            # Send immediately to all connected browsers via WebSocket
            dead_clients = []
            for client in browser_clients:
                try:
                    client.send(json.dumps({"average": average}))
                except Exception:
                    dead_clients.append(client)
            
            # Clean up disconnected browsers
            for client in dead_clients:
                browser_clients.discard(client)

            return jsonify({"status": "success", "average": average}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    except Exception as e:
        print("POST Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


# ==========================================
# Browser WebSocket (Keep this for the App!)
# ==========================================
@sock.route("/ws/browser")
def browser_socket(ws):
    print("Browser connected")
    browser_clients.add(ws)

    # Immediately send current value on connection
    ws.send(json.dumps(latest_data))

    try:
        while True:
            message = ws.receive()
            if message is None:
                break
    except Exception as e:
        print("Browser WebSocket error:", e)
    finally:
        browser_clients.discard(ws)
        print("Browser disconnected")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
