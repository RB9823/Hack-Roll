import base64
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = 'bb85692b080e1bc8c50c18d27e94f3c0f02b85844c283516faf1858ba3342699'
VIRUSTOTAL_SUBMIT_URL = 'https://www.virustotal.com/api/v3/urls'
VIRUSTOTAL_ANALYSES_URL = 'https://www.virustotal.com/api/v3/analyses/{id}'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan_url', methods=['POST'])
def scan_url():
    data = request.json
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400

    url_to_scan = data['url']
    payload = {'url': url_to_scan}
    headers = {
        'accept': 'application/json',
        'x-apikey': API_KEY,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(VIRUSTOTAL_SUBMIT_URL, data=payload, headers=headers)

    if response.status_code == 200:
        analysis_id = response.json()['data']['id']
        return jsonify({'analysis_id': analysis_id}), 200
    else:
        return jsonify({'error': 'Error scanning URL', 'details': response.text}), response.status_code

@app.route('/get_results/<analysis_id>', methods=['GET'])
def get_results(analysis_id):
    headers = {
        'accept': 'application/json',
        'x-apikey': API_KEY,
    }
    result_url = VIRUSTOTAL_ANALYSES_URL.format(id=analysis_id)
    print(result_url)
    response = requests.get(result_url, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Error fetching results', 'details': response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=8000)
