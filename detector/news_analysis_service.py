"""
news_analysis_service.py

Contains the NewsAnalysisService class which can now decide
which model to use based on user input (HF or Gemini).
"""

from .fake_news_detector import FakeNewsDetector
from .gemini_fake_news_detector import GeminiFakeNewsDetector

class NewsAnalysisService:
    """
    Combines the classification result from either the HF pipeline
    or the Gemini approach, plus additional cross-checking logic.
    """

    def __init__(self):
        """
        Initialize one 'permanent' HF detector.
        (Gemini is instantiated on the fly with user-provided keys.)
        """
        self.hf_detector = FakeNewsDetector()

    def analyze_text(self, text: str, model_type: str, gemini_key: str = None):
        """
        Analyzes the text using the chosen model.
        :param text: The user-provided text to classify
        :param model_type: 'hf' or 'gemini'
        :param gemini_key: The API key for Gemini (required if model_type='gemini')
        :return: dict with classification + cross_check info (or error)
        """

        if model_type == "gemini":
            if not gemini_key:
                return {"error": "No Gemini API key provided."}
            # Instantiate a Gemini detector using the user-provided key
            gemini_detector = GeminiFakeNewsDetector(api_key=gemini_key)
            classification = gemini_detector.classify_text(text)
        else:
            # Default to Hugging Face
            classification = self.hf_detector.classify_text(text)

        # Cross-reference step (same placeholder logic as before)
        cross_check_info = self.mock_cross_referencing(text)

        return {
            "classification": classification,
            "cross_check": cross_check_info
        }

    def mock_cross_referencing(self, text: str):
        """
        Example placeholder for real cross-referencing logic.
        """
        if "US" in text or "China" in text:
            return {
                "verified_by": [],
                "explanation": "No reputable mainstream coverage found (mock)."
            }
        else:
            return {
                "verified_by": ["MockNewsSource"],
                "explanation": "No major conflict statements found."
            }
