"""Unit tests for the EmotionDetection package."""

import json
import unittest
from unittest.mock import Mock, patch

from EmotionDetection import emotion_detector


class TestEmotionDetection(unittest.TestCase):
    """Test emotion score parsing and dominant emotion selection."""

    def assert_dominant_emotion(self, statement, expected_emotion):
        """Check the dominant emotion returned for a statement."""
        emotion_names = ("anger", "disgust", "fear", "joy", "sadness")
        emotion_scores = {name: 0.1 for name in emotion_names}
        emotion_scores[expected_emotion] = 0.9
        response_body = json.dumps(
            {"emotionPredictions": [{"emotion": emotion_scores}]}
        )
        response = Mock(text=response_body)

        with patch(
            "final_project.emotion_detection.requests.post",
            return_value=response,
        ) as post_request:
            result = emotion_detector(statement)

        self.assertEqual(result["dominant_emotion"], expected_emotion)
        post_request.assert_called_once()
        self.assertEqual(
            post_request.call_args.kwargs["json"],
            {"raw_document": {"text": statement}},
        )

    def test_joy(self):
        """Test that glad statements return joy as dominant."""
        self.assert_dominant_emotion("I am glad this happened", "joy")

    def test_anger(self):
        """Test that mad statements return anger as dominant."""
        self.assert_dominant_emotion("I am really mad about this", "anger")

    def test_disgust(self):
        """Test that disgusted statements return disgust as dominant."""
        self.assert_dominant_emotion(
            "I feel disgusted just hearing about this", "disgust"
        )

    def test_sadness(self):
        """Test that sad statements return sadness as dominant."""
        self.assert_dominant_emotion("I am so sad about this", "sadness")

    def test_fear(self):
        """Test that afraid statements return fear as dominant."""
        self.assert_dominant_emotion(
            "I am really afraid that this will happen", "fear"
        )

    def test_bad_request_returns_none_scores(self):
        """Return None scores when the emotion service rejects blank text."""
        response = Mock(status_code=400)
        with patch(
            "final_project.emotion_detection.requests.post",
            return_value=response,
        ):
            result = emotion_detector("rejected text")

        self.assertEqual(
            result,
            {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None,
            },
        )
        response.raise_for_status.assert_not_called()

    def test_blank_text_returns_none_without_request(self):
        """Return None scores locally for blank text."""
        with patch("final_project.emotion_detection.requests.post") as post_request:
            result = emotion_detector("  ")

        self.assertIsNone(result["dominant_emotion"])
        self.assertTrue(all(value is None for value in result.values()))
        post_request.assert_not_called()


if __name__ == "__main__":
    unittest.main()
