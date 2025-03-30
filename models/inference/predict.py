"""
Dummy predictor class for development purposes.
"""
import numpy as np
from PIL import Image
import io

class DummyPredictor:
    def __init__(self):
        self.disease_info = {
            'healthy': {
                'description': 'The plant appears to be healthy.',
                'treatments': [],
                'preventive_measures': ['Regular watering', 'Proper sunlight', 'Regular inspection']
            },
            'leaf_blight': {
                'description': 'A fungal disease that causes brown spots on leaves.',
                'treatments': ['Remove affected leaves', 'Apply fungicide', 'Improve air circulation'],
                'preventive_measures': ['Avoid overhead watering', 'Space plants properly', 'Clean garden tools']
            },
            'powdery_mildew': {
                'description': 'A fungal disease that appears as white powdery spots.',
                'treatments': ['Apply neem oil', 'Use sulfur-based fungicide', 'Prune affected areas'],
                'preventive_measures': ['Maintain good air circulation', 'Avoid high humidity', 'Plant resistant varieties']
            }
        }

    def predict(self, image_bytes):
        """
        Dummy prediction function that returns random results.
        """
        try:
            # Verify that the image can be opened
            image = Image.open(io.BytesIO(image_bytes))
            
            # Return random prediction for development
            diseases = list(self.disease_info.keys())
            disease_name = np.random.choice(diseases)
            confidence = float(np.random.uniform(0.6, 0.95))
            
            disease_info = self.disease_info[disease_name]
            
            return {
                "disease_name": disease_name,
                "confidence": confidence,
                "description": disease_info['description'],
                "treatment_recommendations": disease_info['treatments'],
                "preventive_measures": disease_info['preventive_measures']
            }
        except Exception as e:
            raise ValueError(f"Error processing image: {str(e)}")

_predictor = None

def get_predictor():
    """
    Returns a singleton instance of the predictor.
    """
    global _predictor
    if _predictor is None:
        _predictor = DummyPredictor()
    return _predictor 