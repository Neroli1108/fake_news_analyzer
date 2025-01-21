"""
fake_news_detector.py

Contains the FakeNewsDetector class which wraps the zero-shot
classification model from Hugging Face.
"""

from transformers import pipeline

class FakeNewsDetector:
    """
    A simple wrapper around a zero-shot classification model
    from Hugging Face, intended to classify text as 'fake news' or 'real news',
    etc.
    """

    def __init__(self, model_name="facebook/bart-large-mnli"):
        """
        Initialize the zero-shot classification pipeline.
        """
        self.classifier = pipeline(
            "zero-shot-classification",
            model=model_name
        )
        # Define candidate labels for classification
        self.candidate_labels = ["fake news", "real news", "propaganda", "satire"]

    def classify_text(self, text: str):
        """
        Runs zero-shot classification on the given text.
        Returns a dictionary with top label and confidence,
        plus the full result from the pipeline.
        """
        result = self.classifier(
            sequences=text,
            candidate_labels=self.candidate_labels,
            multi_label=False
        )
        # Extract the top-scoring label
        top_label = result["labels"][0]
        top_score = result["scores"][0]

        return {
            "top_label": top_label,
            "confidence": top_score,
            "full_result": result
        }
