document.getElementById('linkForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var userInput = document.getElementById('linkInput').value;
    console.log('User Input:', userInput);

    fetch('/scan_url', {
        method: 'POST',
        headers: {
            'content-type': 'application/json',
        },
        body: JSON.stringify({ url: userInput })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('status').innerText = 'Error';
            document.getElementById('details').innerText = JSON.stringify(data.error);
        } else if (data.analysis_id) {
            document.getElementById('analysis-id').innerText = data.analysis_id;
            document.getElementById('status').innerText = 'Fetching results...';

            return fetch('/get_results/' + data.analysis_id, {
                method: 'GET'
            });
        }
    })
    .then(response => {
        if (response && response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to fetch results');
        }
    })
    .then(resultData => {
        document.getElementById('status').innerText = 'Completed';
        document.getElementById('loading').style.display = 'none';
        document.getElementById('result-message').style.display = 'block';
        document.getElementById('status').innerText = 'Completed';
    
        if (resultData && resultData.data && resultData.data.attributes) {
            const attributes = resultData.data.attributes;
            let detailsHtml = '';
    
            detailsHtml += '<p>Status: ' + attributes.status + '</p>';
    
            if (attributes.stats) {
                detailsHtml += '<p>Stats: </p>';
                detailsHtml += '<ul>';
                detailsHtml += '<li>Harmless: ' + attributes.stats.harmless + '</li>';
                detailsHtml += '<li>Malicious: ' + attributes.stats.malicious + '</li>';
                detailsHtml += '<li>Suspicious: ' + attributes.stats.suspicious + '</li>';
                detailsHtml += '<li>Undetected: ' + attributes.stats.undetected + '</li>';
                detailsHtml += '</ul>';
            }
    
            document.getElementById('details').innerHTML = detailsHtml;
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('status').innerText = 'Error';
        document.getElementById('details').innerText = error.toString();
        document.getElementById('loading').style.display = 'none';
        document.getElementById('result-message').style.display = 'block';
    });    
});
