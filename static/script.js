document.getElementById('inputForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var userInput = document.getElementById('linkInput').value; 

    fetch('/scan_url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: userInput })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json(); // Parses the JSON response
    })
    .then(data => {
        document.getElementById('response').innerText = JSON.stringify(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
