"""
gemini_fake_news_detector.py

Contains the GeminiFakeNewsDetector class, which uses
Google's Gemini model via the google.generativeai library
to analyze news text for possible fake news classification.
"""

import json
import google.generativeai as genai


class GeminiFakeNewsDetector:
    """
    A simple OOP wrapper for Google Gemini (via google.generativeai).
    It prompts the model to classify news text as 'fake news', 'real news',
    etc., and returns a structured result.
    """

    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        """
        Configure the generative AI API and store the model reference.
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def classify_text(self, text: str):
        """
        Call Google Gemini to classify the given text. Returns a dict
        with 'top_label', 'confidence' (if we have it), and 'raw_output'.
        
        Note: Because Gemini is a generative model, you’ll need to design
        a prompt carefully to extract a classification label. This example
        uses a simplified approach that asks for JSON output.
        """
        # Example prompt that instructs the model to output JSON
        prompt = f"""
        You are an AI that classifies short news statements into categories:
        ['fake news', 'real news', 'propaganda', 'satire'].

        Please analyze the following text and output valid JSON with two fields:
        "label" (one of: fake news, real news, propaganda, satire)
        and "rationale" (a short explanation).

        Text: \"{text}\"

        Output format example:
        {{
          "label": "fake news",
          "rationale": "Because it contradicts verified sources..."
        }}
        """

        # Call the model
        response = self.model.generate_content(prompt)

        # The entire model output is in response.text
        raw_output = response.text.strip()

        # Try to parse JSON from the output (the model might not return valid JSON every time!)
        label = "unknown"
        rationale = "No valid JSON found."

        try:
            parsed = json.loads(raw_output)
            label = parsed.get("label", "unknown")
            rationale = parsed.get("rationale", "No rationale provided.")
        except json.JSONDecodeError:
            pass  # Fallback to the raw output or an error message

        # For demonstration, we don't have a “confidence” from Gemini directly.
        # You could do a follow-up prompt or add heuristics. We'll just set 1.0 or 0.0 arbitrarily.
        confidence = 1.0 if label != "unknown" else 0.0

        return {
            "top_label": label,
            "confidence": confidence,
            "raw_output": raw_output,
            "rationale": rationale
        }
