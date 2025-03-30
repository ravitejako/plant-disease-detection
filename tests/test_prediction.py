import pytest
from fastapi.testclient import TestClient
from api.main import app
import io
from PIL import Image
import numpy as np

client = TestClient(app)

@pytest.fixture
def sample_image():
    # Create a dummy image for testing
    img = Image.new('RGB', (224, 224), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

def test_predict_endpoint(sample_image):
    response = client.post(
        "/api/v1/predict",
        files={"file": ("test.png", sample_image, "image/png")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "disease_name" in data
    assert "confidence" in data
    assert "treatment_recommendations" in data

def test_invalid_file_type():
    response = client.post(
        "/api/v1/predict",
        files={"file": ("test.txt", b"test content", "text/plain")}
    )
    assert response.status_code == 400
    assert "File must be an image" in response.json()["detail"]

def test_get_supported_diseases():
    response = client.get("/api/v1/diseases")
    assert response.status_code == 200
    data = response.json()
    assert "diseases" in data
    assert len(data["diseases"]) > 0
    
    # Check disease object structure
    disease = data["diseases"][0]
    assert "name" in disease
    assert "description" in disease
    assert "symptoms" in disease
    assert "treatments" in disease
    assert "preventive_measures" in disease 