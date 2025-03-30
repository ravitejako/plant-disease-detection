from pydantic import BaseModel
from typing import List, Optional

class PredictionResponse(BaseModel):
    disease_name: str
    confidence: float
    description: str
    treatment_recommendations: List[str]
    preventive_measures: List[str]

class Disease(BaseModel):
    name: str
    description: str
    symptoms: List[str]
    treatments: List[str]
    preventive_measures: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Leaf Blight",
                "description": "A fungal disease that causes brown spots on leaves",
                "symptoms": ["Brown spots", "Yellowing leaves", "Leaf wilting"],
                "treatments": ["Apply fungicide", "Remove infected leaves"],
                "preventive_measures": ["Proper spacing", "Regular inspection"]
            }
        } 