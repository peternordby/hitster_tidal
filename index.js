const backendurl = 'http://127.0.0.1:5000'

let onScanSuccess = (decodedText, decodedResult) => {
    // Handle on success condition with the decoded text or result.
    // If decodedText can be converted to a valid URL, you can use this value to
    // redirect the user to the URL.
    console.log(`Scan result: ${decodedText}`);
    htmlscanner.clear();

    // Assuming the parsed text is a URL, send get request to backend
    if (decodedText.startsWith("https://app.hitsternordics.com")) {
        console.log("Requesting backend");
        xhr = new XMLHttpRequest();
        xhr.open("GET", backendurl + '?link=' + decodedText);
        xhr.send();
        xhr.resonseType = 'json';
        xhr.onload = () => {
            if (xhr.status == 200) {
                console.log(xhr.response);
                // Open in new tab
                window.open(xhr.response);
            }
            else {
                console.log("Error: " + xhr.status);
            }
        }
        console.log("Backend request sent");
    }
}

let scanButton = document.getElementById("scan");
scanButton.onclick = () => {
    htmlscanner.render(onScanSuccess);
}

let htmlscanner = new Html5QrcodeScanner(
    "my-qr-reader",
    { fps: 10, qrbos: 250 }
);