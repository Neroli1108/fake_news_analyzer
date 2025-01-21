"""
app.py

Main Flask application. A single endpoint (/analyze) that
switches between Hugging Face and Gemini based on user input.
"""

from flask import Flask, request, render_template_string, jsonify
from detector.news_analysis_service import NewsAnalysisService

app = Flask(__name__)

# Create one shared service instance
analysis_service = NewsAnalysisService()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Fake News Detection</title>
    <style>
       body { font-family: Arial, sans-serif; margin: 40px; }
       .container { margin-bottom: 40px; border: 1px solid #ccc; padding: 20px; }
       label, input, textarea, button { display: block; margin: 10px 0; }
       #result { margin-top: 20px; }
       .result-section { border: 1px solid #ccc; padding: 10px; margin-top: 10px; }
       pre { background-color: #f8f8f8; padding: 10px; }
    </style>
</head>
<body>
    <h1>Fake News Detection</h1>
    <div class="container">
      <p>Select which model to use:</p>
      <label>
        <input type="radio" name="modelType" value="hf" checked />
        Hugging Face
      </label>
      <label>
        <input type="radio" name="modelType" value="gemini" />
        Gemini
      </label>

      <p>Gemini API Key (only needed if Gemini is selected):</p>
      <input type="text" id="geminiKey" placeholder="Enter Gemini key if using Gemini" />

      <p>Paste news content:</p>
      <textarea id="newsText" rows="4" cols="60" placeholder="Paste text here..."></textarea>
      <button onclick="analyzeText()">Analyze</button>
    </div>

    <div id="result"></div>

    <script>
    async function analyzeText() {
        const text = document.getElementById('newsText').value.trim();
        if (!text) {
            alert('Please paste some text first!');
            return;
        }
        // Determine which model is selected
        const modelType = document.querySelector('input[name="modelType"]:checked').value;
        // If the user chose Gemini, get the key
        let geminiKey = "";
        if (modelType === "gemini") {
            geminiKey = document.getElementById('geminiKey').value.trim();
            if (!geminiKey) {
                alert('Gemini key is required if using Gemini model.');
                return;
            }
        }

        // Send the text, modelType, and geminiKey to /analyze
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                model_type: modelType,
                gemini_key: geminiKey
            })
        });

        const data = await response.json();
        displayResult(data);
    }

    function displayResult(data) {
        let resultDiv = document.getElementById('result');
        resultDiv.innerHTML = '';

        if (data.error) {
            resultDiv.innerHTML = '<p style="color:red;">Error: ' + data.error + '</p>';
            return;
        }

        // Classification
        let classificationHtml = `
          <div class="result-section">
            <h2>Classification Result</h2>
            <p><strong>Label:</strong> ${data.classification.top_label}</p>
            <p><strong>Confidence:</strong> ${data.classification.confidence.toFixed(3)}</p>
          </div>
        `;

        // Cross-check
        let crossCheckHtml = `
          <div class="result-section">
            <h2>Cross-Reference Check</h2>
            <p><strong>Verified By:</strong> ${
              data.cross_check.verified_by 
              ? data.cross_check.verified_by.join(', ') 
              : 'None'
            }</p>
            <p><strong>Explanation:</strong> ${data.cross_check.explanation}</p>
          </div>
        `;

        // Debug info
        let debugSection = '';
        if (data.classification.raw_output) {
            debugSection = `
            <div class="result-section">
              <h2>Model Raw Output (Gemini or other LLM)</h2>
              <pre>${data.classification.raw_output}</pre>
            </div>`;
        } else if (data.classification.full_result) {
            let fullResult = JSON.stringify(
                data.classification.full_result, null, 2
            );
            debugSection = `
            <div class="result-section">
              <h2>Debug Info (HF Zero-shot Output)</h2>
              <pre>${fullResult}</pre>
            </div>`;
        }

        resultDiv.innerHTML = classificationHtml + crossCheckHtml + debugSection;
    }
    </script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    A single endpoint that looks at model_type and gemini_key,
    then delegates to NewsAnalysisService.
    """
    data = request.get_json()
    text = data.get("text", "").strip()
    model_type = data.get("model_type", "hf")
    gemini_key = data.get("gemini_key", None)

    if not text:
        return jsonify({"error": "No text provided."}), 400

    # Call our analysis service, specifying the chosen model
    result = analysis_service.analyze_text(
        text=text,
        model_type=model_type,
        gemini_key=gemini_key
    )

    # If there's an error (e.g. no Gemini key provided), handle it
    if "error" in result:
        return jsonify({"error": result["error"]}), 400

    return jsonify(result), 200


if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True)
