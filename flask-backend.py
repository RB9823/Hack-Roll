from flask import Flask, request, jsonify
import requests


app = Flask(__name__)

API_KEY = 'bb85692b080e1bc8c50c18d27e94f3c0f02b85844c283516faf1858ba3342699'
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
