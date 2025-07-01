from fastapi.testclient import TestClient
from api.routes.predict import predict_router
from models import SentimentRequest

client = TestClient(predict_router)

def test_analyze_sentiment_positive():
    """Test analyze_sentiment with positive sentiment text."""
    request_data = SentimentRequest(text="I love this product! It's amazing.")
    response = client.post("/analyze/", json=request_data.dict())
    assert response.status_code == 200
    response_data = response.json()
    assert "label" in response_data
    assert "confidence" in response_data
    assert response_data["label"] == "positive"

def test_analyze_sentiment_negative():
    """Test analyze_sentiment with negative sentiment text."""
    request_data = SentimentRequest(text="I hate this product. It's terrible.")
    response = client.post("/analyze/", json=request_data.dict())
    assert response.status_code == 200
    response_data = response.json()
    assert "label" in response_data
    assert "confidence" in response_data
    assert response_data["label"] == "negative"

def test_analyze_sentiment_empty_text():
    """Test analyze_sentiment with empty text."""
    request_data = SentimentRequest(text="")
    response = client.post("/analyze/", json=request_data.dict())
    assert response.status_code == 422  # Unprocessable Entity for invalid input

def test_analyze_sentiment_model_not_loaded():
    """Test analyze_sentiment when the model is not loaded."""
    global sentiment_model
    sentiment_model = None  # Simulate model not being loaded
    request_data = SentimentRequest(text="This is a test.")
    response = client.post("/analyze/", json=request_data.dict())
    assert response.status_code == 500
    assert "Model loading failed" in response.json()["detail"]