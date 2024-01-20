from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = CORS(Flask(__name__))

API_KEY = os.getenv('VIRUSTOTAL_API_KEY') #set the api key in your local env
VIRUSTOTAL_URL = 'https://www.virustotal.com/api/v3/urls'

@app.route('/scan_url', methods=['POST'])
def scan_url():
    url_to_scan = request.json.get('url')
    if not url_to_scan:
        return jsonify({'error': 'No URL provided'}), 400

    headers = {
        'accept': 'application/json',
        'x-apikey': API_KEY
    }
    payload = {'url': url_to_scan}

    response = requests.post(VIRUSTOTAL_URL, data=payload, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Error scanning URL'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
