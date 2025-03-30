from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Plant Disease Detection API"
    DEBUG: bool = True
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React frontend
        "http://localhost:8000",  # FastAPI backend
        "http://localhost:8001",  # Alternative FastAPI backend port
        "http://127.0.0.1:3000",  # React frontend alternative
        "http://127.0.0.1:8000",  # FastAPI backend alternative
        "http://127.0.0.1:8001",  # Alternative FastAPI backend port alternative
    ]
    
    # Database Configuration
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "plant_disease_db")
    
    # Model Configuration
    MODEL_PATH: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                 "models", "plant_disease_model.h5")
    IMAGE_SIZE: int = 224  # Input image size for the model
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    
    class Config:
        case_sensitive = True

settings = Settings() 