document.getElementById('linkForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var userInput = document.getElementById('linkInput').value;
    fetch('/scan_url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: userInput })
    })
    .then(response => response.json())
    .then(data => {
        // Assuming 'data' is the object containing the response from your Flask backend
        if (data.analysis_id) {
            document.getElementById('analysis-id').innerText = data.analysis_id;
        }
        if (data.error) {
            document.getElementById('status').innerText = 'Error';
            document.getElementById('details').innerText = JSON.stringify(data.error);
        } else {
            document.getElementById('status').innerText = 'Success';
            // You can add more details or handle other response data here
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('status').innerText = 'Error';
        document.getElementById('details').innerText = error.toString();
    });
});


