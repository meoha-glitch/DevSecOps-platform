from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify(status="ok"), 200

@app.route("/")
def hello():
    version = os.environ.get("APP_VERSION", "dev")
    return jsonify(
        message="Bienvenue sur la plateforme DevSecOps",
        version=version
    ), 200

import subprocess

@app.route("/debug")
def debug():
    cmd = "echo test"
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result.stdout

def calculate_discount(price, percentage):
    if percentage > 50:
        final_price = price - (price * percentage / 100)
        if final_price < 0:
            final_price = 0
        return final_price
    elif percentage > 20:
        return price * 0.8
    else:
        return price * 0.95

@app.route("/discount")
def discount():
    return jsonify(price=calculate_discount(100, 30)), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
