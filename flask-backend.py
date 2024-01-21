from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
app =CORS(app)

API_KEY = os.getenv('VIRUSTOTAL_API_KEY') #set the api key in your local env
VIRUSTOTAL_URL = 'https://www.virustotal.com/api/v3/urls'

@app.route('/scan_url', methods=['POST'])
def scan_url():
    url_to_scan = request.json.get('url')
    payload = {'url': url_to_scan}
    response = requests.post(VIRUSTOTAL_URL, data=payload, headers=headers)
    if not url_to_scan:
        return jsonify({'error': 'No URL provided'}), 400

    headers = {
        'accept': 'application/json',
        'x-apikey': API_KEY,
        'content-type': 'application/x-www-form-urlencoded' 
    }

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Error scanning URL'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
