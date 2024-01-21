// html element id is inputForm
document.getElementById('linkForm').addEventListener('submit', function(event)  {
    event.preventDefault();
    // stores the url string from html text box with id textInput
    var userInput = document.getElementById('textInput').value;

    // /scan_url is the flask app endpoint
    fetch('/scan_url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: userInput })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('response').innerText = data.result;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});
