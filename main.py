from flask import Flask, request, jsonify
import time
import threading

app = Flask(__name__)

# Rate limiter storage
last_request_time = 0
lock = threading.Lock()
cooldown_seconds = 2  # Accept only 1 request every 2 seconds

@app.route('/btc-signal', methods=['POST'])
def btc_signal():
    global last_request_time
    with lock:
        now = time.time()
        if now - last_request_time < cooldown_seconds:
            return jsonify({"error": "Too many requests – slow down"}), 429
        last_request_time = now

    data = request.get_json()
    print("✅ Received from EA:", data)

    # Basic AI-mock logic (you can replace this later)
    try:
        price = data['price']
        ai_response = {
            "action": "BUY",
            "entry": round(price),
            "tp": round(price + 170),
            "sl": round(price - 170)
        }
        return jsonify(ai_response)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/', methods=['GET'])
def index():
    return "🚀 BTCUSD AI Signal Receiver Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
