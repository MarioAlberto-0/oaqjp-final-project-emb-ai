"""Emotion detection client for the Watson NLP service."""

import json

import requests


def emotion_detector(text_to_analyze):
    """Return emotion scores and the dominant emotion for the input text."""
    if not isinstance(text_to_analyze, str):
        raise ValueError("Text to analyze must be a string.")

    emotion_names = ("anger", "disgust", "fear", "joy", "sadness")
    if not text_to_analyze.strip():
        return {name: None for name in (*emotion_names, "dominant_emotion")}

    url = (
        "https://sn-watson-emotion.labs.skills.network/v1/"
        "watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    input_json = {"raw_document": {"text": text_to_analyze}}

    response = requests.post(url, json=input_json, headers=headers, timeout=30)
    if response.status_code == 400:
        return {name: None for name in (*emotion_names, "dominant_emotion")}

    response.raise_for_status()
    result = json.loads(response.text)
    if not isinstance(result, dict):
        raise ValueError("The emotion service returned an invalid response.")

    predictions = result.get("emotionPredictions")
    if not isinstance(predictions, list) or not predictions:
        raise ValueError("The emotion service returned no predictions.")

    prediction = predictions[0]
    if not isinstance(prediction, dict):
        raise ValueError("The emotion service returned an invalid prediction.")

    emotions = prediction.get("emotion")
    if not isinstance(emotions, dict) or any(
        not isinstance(emotions.get(name), (int, float))
        for name in emotion_names
    ):
        raise ValueError("The emotion service returned incomplete emotion scores.")

    scores = {name: emotions[name] for name in emotion_names}
    scores["dominant_emotion"] = max(emotion_names, key=scores.get)
    return scores
