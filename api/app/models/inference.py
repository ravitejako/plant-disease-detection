import tensorflow as tf
import numpy as np
from PIL import Image
from typing import Tuple, Dict
import io

class PlantDiseaseModel:
    def __init__(self, model_path: str, image_size: Tuple[int, int] = (224, 224)):
        self.model_path = model_path
        self.image_size = image_size
        self.model = None
        self.class_names = [
            "healthy",
            "leaf_blight",
            "leaf_rust",
            "leaf_spot",
            # Add more classes as needed
        ]
        self.load_model()

    def load_model(self):
        try:
            self.model = tf.keras.models.load_model(self.model_path)
        except Exception as e:
            print(f"Error loading model: {e}")
            # For development, create a dummy model
            self.model = self._create_dummy_model()

    def _create_dummy_model(self):
        # Temporary dummy model for development
        inputs = tf.keras.Input(shape=(*self.image_size, 3))
        x = tf.keras.layers.Conv2D(32, 3, activation='relu')(inputs)
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        outputs = tf.keras.layers.Dense(len(self.class_names), activation='softmax')(x)
        return tf.keras.Model(inputs, outputs)

    def preprocess_image(self, image_data: bytes) -> np.ndarray:
        """Preprocess image for model input."""
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image
        image = image.resize(self.image_size)
        
        # Convert to numpy array and normalize
        image_array = np.array(image) / 255.0
        
        # Add batch dimension
        return np.expand_dims(image_array, axis=0)

    def predict(self, image_data: bytes) -> Dict:
        """Predict disease from image data."""
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image_data)
            
            # Make prediction
            predictions = self.model.predict(processed_image)
            
            # Get predicted class and confidence
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            
            # Get disease name
            disease_name = self.class_names[predicted_class_idx]
            
            return {
                "disease_name": disease_name,
                "confidence": confidence,
                "description": "Description placeholder",  # To be replaced with actual description
                "treatment_recommendations": [
                    "Treatment recommendation placeholder"  # To be replaced with actual recommendations
                ],
                "preventive_measures": [
                    "Preventive measure placeholder"  # To be replaced with actual measures
                ]
            }
        except Exception as e:
            raise Exception(f"Error during prediction: {str(e)}")

# Create singleton instance
model_instance = None

def get_model(model_path: str) -> PlantDiseaseModel:
    global model_instance
    if model_instance is None:
        model_instance = PlantDiseaseModel(model_path)
    return model_instance 