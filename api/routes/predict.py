from fastapi import APIRouter, HTTPException
from models import SentimentRequest, SentimentResponse
from ai.model_loader import ModelLoader, ModelSelection
from functools import wraps


predict_router = APIRouter()

sentiment_model = None

def ensure_model_loaded(func):
    """Decorator to ensure the model is loaded before executing the route."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Decorator to ensure the model is loaded before executing the route.

        If the model is not loaded, it will load it and store it in the global
        variable `sentiment_model`. This allows the model to be reused across
        different requests.

        Args:
            *args: Arguments passed to the route function.
            **kwargs: Keyword arguments passed to the route function.

        Returns:
            The return value of the route function.
        """
        global sentiment_model
        if sentiment_model is None:
            # Create a model loader and load the model.
            # Store it in the global variable so it can be reused.
            sentiment_model = ModelLoader()
            sentiment_model.load_model()
        # Call the route function with the loaded model.
        return func(*args, **kwargs)
    return wrapper



@predict_router.post("/analyze/", response_model=SentimentResponse)
@ensure_model_loaded
def analyze_sentiment(request_data: SentimentRequest) -> SentimentResponse:
    """Analyzes the sentiment of a given text and returns the sentiment scores.

    Args:
        request_data (SentimentRequest): The text to analyze.

    Returns:
        SentimentResponse: The sentiment scores.
    """

    try:
        # Call the predict method to get the sentiment scores
        predictions = sentiment_model.predict(request_data.text)
    except Exception as e:
        # Raise an HTTPException if the model fails to load
        raise HTTPException(status_code=500, detail=f"Model loading failed: {e}")

    # Return the predictions as a SentimentResponse
    return SentimentResponse(**predictions)
 

