from flask import Flask, jsonify
import os

app = Flask(__name__)
from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app)
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
