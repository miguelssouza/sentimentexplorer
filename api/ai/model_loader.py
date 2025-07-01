
from enum import Enum
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
from scipy.special import softmax


class ModelSelection(str, Enum):
    """Enum for model selection."""
    TWITTER_ROBERTA = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    MULTILINGUAL_BERT = "tabularisai/multilingual-sentiment-analysis"
    


class ModelLoader:
    def __init__(self, model:ModelSelection = ModelSelection.MULTILINGUAL_BERT):
        self.model_name = model.value
        self.tokenizer = None
        self.config = None
        self.model = None
    
    def load_model(self):
        """Load the model and tokenizer."""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.config = AutoConfig.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")
    def predict(self, text: str) -> dict:
        """Predict sentiment for a given text."""
        if self.tokenizer is None or self.model is None:
            raise RuntimeError("Model and tokenizer must be loaded before prediction.")

        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = self.model(**inputs)
        scores = outputs.logits.detach().numpy()
        scores = softmax(scores, axis=1)[0]

        labels = self.config.id2label
        sentiment = {labels[i]: scores[i] for i in range(len(labels))}
        predicted_label = max(sentiment, key=sentiment.get)
        sentiment_prediction_data = {
            "text": text,
            "predicted_label": predicted_label,
            "scores": sentiment
        }
        
        return sentiment_prediction_data