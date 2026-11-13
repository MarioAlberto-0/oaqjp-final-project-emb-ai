function RunSentimentAnalysis() {
    const textToAnalyze = document.getElementById("textToAnalyze").value.trim();
    const systemResponse = document.getElementById("system_response");

    if (!textToAnalyze) {
        systemResponse.textContent = "Invalid text! Please try again!";
        return;
    }

    let xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        systemResponse.textContent = xhttp.responseText;
    };
    xhttp.onerror = function() {
        systemResponse.textContent = "Unable to contact the emotion detection service.";
    };
    xhttp.open(
        "GET",
        `/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`,
        true
    );
    xhttp.send();
}
