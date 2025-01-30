from flask import Flask, jsonify
from flask_cors import CORS
from polygon import RESTClient
import json

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
api_key = "gr_c53GdKGANspfwSpkrg3VxN2Jkhwc_"

@app.route('/api/aggs', methods=["GET"])
def get_aggs():
    client = RESTClient(api_key)  # Initialize the REST client

    try:
        # Attempt to fetch data
        aggs = list(client.get_aggs(
            "AAPL",
            1,
            "day",
            "2025-01-01",
            "2025-01-22"
        ))



        if not aggs:
            return jsonify({"error": "No data available"}), 404

        return jsonify(aggs)

    except Exception as e:
        print("FULL ERROR TRACEBACK:", str(e))  # Log full error details
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
