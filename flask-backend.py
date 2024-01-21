from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv('VIRUSTOTAL_API_KEY') #set the api key in your local env
VIRUSTOTAL_URL = 'https://www.virustotal.com/api/v3/urls'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan_url', methods=['POST'])
def scan_url():
    url_to_scan = request.json.get('url')
    headers = {
        'accept': 'application/json',
        'x-apikey': API_KEY,
        'content-type': 'application/x-www-form-urlencoded' 
    }

    if not url_to_scan:
        return jsonify({'error': 'No URL provided'}), 400

    payload = {'url': url_to_scan}
    response = requests.post(VIRUSTOTAL_URL, data=payload, headers=headers)

    if response.status_code == 200:
        analysis_id = response.json()['data']['id']
        return jsonify({'analysis_id': analysis_id}), 200
    else:
        return jsonify({'error': 'Error scanning URL', 'details': response.text}), response.status_code

@app.route('/get_results/<analysis_id>', methods=['GET'])
def get_results(analysis_id):
    headers = {
        'accept': 'application/json',
        'x-apikey': API_KEY
    }
    result_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    response = requests.get(result_url, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Error fetching results', 'details': response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port = 8000)
