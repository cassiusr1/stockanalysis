import requests
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
from polygon import RESTClient
import test
import json
from flask_cors import cross_origin
from typing import cast
from urllib3 import HTTPResponse



app = Flask(__name__)
CORS(app, resources={r"/": {"origins": ""}}, supports_credentials=True)
api_key = "gr_c53GdKGANspfwSpkrg3VxN2Jkhwc_"




@app.route('/api/aggs', methods=["GET", "OPTIONS"])
@cross_origin()
def get_aggs():
    if request.method == "OPTIONS":  # Handle preflight request
        return jsonify({"message": "CORS preflight successful"}), 200
    client = RESTClient(test.api_key)

    aggs = cast(
        HTTPResponse,
        client.get_aggs(
            'AAPL',
            1,
            'day',
            '2025-01-01',
            '2025-01-22',
            raw=True

        )
    )

    data = json.loads(aggs.data)
    aggregate = data.get('results', [])

    if aggregate:
        df = pd.DataFrame(aggregate)
        df['timestamp'] = pd.to_datetime(df['t'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')  # Convert timestamp
        df.set_index('timestamp', inplace=True)
        df.drop('t', axis=1, inplace=True)
        df.rename(columns={
            'timestamp': 'Date',
            'o': 'Open',
            'h': 'High',
            'l': 'Low',
            'c': 'Close',
            'v': 'Volume',
            'vw': 'Volume Weighted',
            'n': 'Number of Transactions',



        }, inplace=True)

        # Convert DataFrame to a JSON serializable format
        return jsonify(df.to_dict(orient="records"))
    else:
        return jsonify({"error": "No data available"})




# @app.route('/api/data')
# def get_data():
#     # Polygon.io API endpoint for intraday data (1-minute intervals, for example)
#     url = f'https://api.polygon.io/v2/aggs/ticker/IBM/prev?apiKey=gr_c53GdKGANspfwSpkrg3VxN2Jkhwc_'
#     response = requests.get(url)
#
#
#     # Check if the request was successful
#     if response.status_code == 200:
#         data = response.json()
#
#         # Example: Parsing the response into a DataFrame
#         # You may need to adjust this depending on the structure of the response from Polygon.io
#         timeseries = data.get('results', [])
#
#         if timeseries:
#             df = pd.DataFrame(timeseries)
#             df['timestamp'] = pd.to_datetime(df['t'], unit='ms')
#             df.set_index('timestamp', inplace=True)
#             df.drop('t', axis=1, inplace=True)
#             df.rename(columns={
#                 'o': 'Open',
#                 'h': 'High',
#                 'l': 'Low',
#                 'c': 'Close',
#                 'v': 'Volume'
#             }, inplace=True)
#
#             # Convert DataFrame to a JSON serializable format
#             return jsonify(df.to_dict(orient="split"))
#         else:
#             return jsonify({"error": "No data available"})
#
#     return jsonify({"error": "Failed to fetch data from Polygon.io"}), 500

if __name__ == '__main__':
    app.run(debug=True)


