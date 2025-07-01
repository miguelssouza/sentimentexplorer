from os import environ
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
from routes.predict import predict_router

# Load environment variables
load_dotenv()

# Get environment variables
PORT=environ.get("PORT")

app = FastAPI(title="Sentiment Prediction API", version="1.0.0")

# Include routes
app.include_router(predict_router)

@app.get("/")
def read_root():
    """
    Welcome message
    """
    return {"message": "Welcome to the Sentiment Prediction API!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")

