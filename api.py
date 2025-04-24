from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from utils import mask_pii
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Email Classifier API",
    description="API for classifying emails and masking PII",
)

try:
    model = joblib.load("model/email_classifier.pkl")
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    model = None

class EmailRequest(BaseModel):
    email_body: str

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Email Classification API is running", "docs": "/docs"}

@app.post("/classify")
def classify_email(request: EmailRequest):
    logger.info("Classify endpoint accessed")
    email = request.email_body

    try:
        # Step 1: Mask PII
        masked_email, entity_list = mask_pii(email)
        logger.info("PII masking completed")

        # Step 2: Predict category
        if model is None:
            raise ValueError("Model not loaded")
        category = model.predict([masked_email])[0]
        logger.info(f"Email classified as: {category}")

        # Step 3: Format response as required
        response = {
            "input_email_body": email,
            "list_of_masked_entities": entity_list,
            "masked_email": masked_email,
            "category_of_the_email": category
        }
        logger.info("Response prepared successfully")
        return response
    except Exception as e:
        logger.error(f"Error in classify_email: {str(e)}")
        raise

logger.info("FastAPI app initialized")
