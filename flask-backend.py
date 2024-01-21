import base64
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = 'bb85692b080e1bc8c50c18d27e94f3c0f02b85844c283516faf1858ba3342699' #os.getenv('VIRUSTOTAL_API_KEY') set the api key in your local env
VIRUSTOTAL_URL = 'https://www.virustotal.com/api/v3/urls'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan_url', methods=['POST'])
def scan_url():
    print("Received Content-Type:", request.content_type)  # Debug line
    data = request.json
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400

    payload = {'url': url_to_scan}

    #url_to_scan = data['url']
    #url_id = base64.urlsafe_b64encode(url_to_scan.encode()).decode().rstrip('=')

    headers = {
        'accept': 'application/json',
        'x-apikey': API_KEY,
        'Content-Type': 'application/json'
    }

    #payload = {'url': url_id}
    response = requests.post(VIRUSTOTAL_URL, headers=headers, json=payload)

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
    result_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    response = requests.get(result_url, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Error fetching results', 'details': response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port = 8000)
