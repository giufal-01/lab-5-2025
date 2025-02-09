from flask import Flask, request, jsonify
import json

app = Flask(__name__)

LOG_FILE = "operations.json"

@app.route("/notify", methods=["POST"])
def notify():
    data = request.json
    with open(LOG_FILE, "a") as f:
        json.dump(data, f)
        f.write("\n")
    return jsonify({"message": "Saved"}), 200

@app.route("/last", methods=["GET"])
def last_operations():
    try:
        with open(LOG_FILE, "r") as f:
            operations = [json.loads(line) for line in f]
    except FileNotFoundError:
        operations = []
    return jsonify({"operations": operations})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
