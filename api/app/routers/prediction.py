from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from models.inference.predict import get_predictor
from app.schemas.prediction import PredictionResponse
from app.schemas.user import User
from app.core.config import settings
from app.core.auth import get_current_active_user
from app.core.database import db
from datetime import datetime
from bson import ObjectId
import logging
import sys
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(project_root))

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict_disease(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """
    Predict plant disease from uploaded image
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read file contents
        contents = await file.read()
        
        # Get predictor instance
        predictor = get_predictor()
        
        # Make prediction
        try:
            prediction = predictor.predict(contents)
            
            # Store prediction in database
            predictions_collection = db.get_db()["predictions"]
            prediction_doc = {
                "id": str(ObjectId()),
                "user_id": current_user.id,
                "filename": file.filename,
                "disease_name": prediction["disease_name"],
                "confidence": prediction["confidence"],
                "timestamp": datetime.utcnow(),
                "metadata": {
                    "file_size": len(contents),
                    "content_type": file.content_type
                }
            }
            await predictions_collection.insert_one(prediction_doc)
            
            return PredictionResponse(**prediction)
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Error processing image. Please try again."
            )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/diseases")
async def get_supported_diseases(current_user: User = Depends(get_current_active_user)):
    """
    Get list of supported plant diseases
    """
    try:
        predictor = get_predictor()
        diseases = []
        
        for disease_name, info in predictor.disease_info.items():
            if disease_name != 'healthy':
                diseases.append({
                    'name': disease_name,
                    'description': info['description'],
                    'symptoms': [
                        'Visible spots on leaves',
                        'Discoloration',
                        'Wilting'
                    ],  # These would ideally come from a database
                    'treatments': info['treatments'],
                    'preventive_measures': info['preventive_measures']
                })
        
        return {'diseases': diseases}
    
    except Exception as e:
        logger.error(f"Error fetching diseases: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching disease information")

@router.get("/predictions/history")
async def get_prediction_history(current_user: User = Depends(get_current_active_user)):
    """
    Get prediction history for the current user
    """
    try:
        predictions_collection = db.get_db()["predictions"]
        cursor = predictions_collection.find({"user_id": current_user.id})
        predictions = []
        
        async for prediction in cursor:
            predictions.append({
                "id": prediction["id"],
                "disease_name": prediction["disease_name"],
                "confidence": prediction["confidence"],
                "timestamp": prediction["timestamp"],
                "filename": prediction["filename"]
            })
        
        return {"predictions": predictions}
    
    except Exception as e:
        logger.error(f"Error fetching prediction history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error fetching prediction history"
        ) 