# Plant Disease Detection System

A deep learning-based system for detecting and classifying plant diseases using computer vision techniques. This project uses a ResNet50 model trained on the PlantVillage dataset to identify various plant diseases.

## Features

- Real-time plant disease detection
- Support for multiple plant types and diseases
- Detailed disease information and treatment recommendations
- User-friendly web interface
- RESTful API for model inference

## Supported Plants and Diseases

The system currently supports the following plants and their diseases:

1. Apple
   - Apple Scab
   - Black Rot
   - Cedar Apple Rust
   - Healthy

2. Blueberry
   - Healthy

3. Cherry
   - Powdery Mildew
   - Healthy

4. Corn (Maize)
   - Cercospora Leaf Spot
   - Common Rust
   - Northern Leaf Blight
   - Healthy

5. Grape
   - Black Rot
   - Esca (Black Measles)
   - Leaf Blight
   - Healthy

6. Orange
   - Huanglongbing (Citrus Greening)

7. Peach
   - Bacterial Spot
   - Healthy

8. Pepper
   - Bacterial Spot
   - Healthy

9. Potato
   - Early Blight
   - Late Blight
   - Healthy

10. Raspberry
    - Healthy

11. Soybean
    - Healthy

12. Squash
    - Powdery Mildew

13. Strawberry
    - Leaf Scorch
    - Healthy

14. Tomato
    - Bacterial Spot
    - Early Blight
    - Late Blight
    - Leaf Mold
    - Septoria Leaf Spot
    - Spider Mites
    - Target Spot
    - Yellow Leaf Curl Virus
    - Mosaic Virus
    - Healthy

## Project Structure

```
plant/
├── api/                    # FastAPI backend
│   ├── app/
│   │   ├── routers/       # API routes
│   │   ├── schemas/       # Pydantic models
│   │   └── main.py        # FastAPI application
│   └── requirements.txt    # Backend dependencies
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/        # Page components
│   │   └── App.js        # Main App component
│   └── package.json       # Frontend dependencies
├── models/                # ML model and utilities
│   ├── data_loader.py    # Dataset loading utilities
│   ├── model.py          # Model architecture
│   ├── trainer.py        # Training utilities
│   └── disease_info.json # Disease information database
└── train.py              # Training script
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/plant-disease-detection.git
cd plant-disease-detection
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install backend dependencies:
```bash
cd api
pip install -r requirements.txt
```

4. Install frontend dependencies:
```bash
cd frontend
npm install
```

## Usage

### Training the Model

1. Prepare your dataset in the following structure:
```
dataset/
├── train/
│   ├── plant_disease/
│   └── healthy/
├── valid/
│   ├── plant_disease/
│   └── healthy/
└── test/
    ├── plant_disease/
    └── healthy/
```

2. Train the model:
```bash
python train.py --data_dir path/to/dataset --num_epochs 20 --batch_size 32
```

### Running the Application

1. Start the backend server:
```bash
cd api
uvicorn app.main:app --reload
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

3. Open your browser and navigate to `http://localhost:3000`

## API Documentation

The API documentation is available at `http://localhost:8000/docs` when the backend server is running.

### Endpoints

- `POST /api/predict`: Upload an image for disease prediction
- `GET /api/diseases`: Get list of supported diseases
- `GET /api/diseases/{disease_name}`: Get detailed information about a specific disease

## Model Architecture

The system uses a ResNet50 model with the following modifications:
- Pretrained on ImageNet
- Modified final layer for plant disease classification
- Dropout for regularization
- Data augmentation for better generalization

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [PlantVillage Dataset](https://www.kaggle.com/datasets/emmarex/plantdisease)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [PyTorch](https://pytorch.org/) 