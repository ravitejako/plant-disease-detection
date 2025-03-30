import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import os
import requests
import zipfile
from pathlib import Path
import shutil
from sklearn.model_selection import train_test_split
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlantDiseaseTrainer:
    def __init__(self, data_dir='data', img_size=(224, 224)):
        self.data_dir = Path(data_dir)
        self.img_size = img_size
        self.model = None
        self.class_names = []
        
    def download_dataset(self, url):
        """Download and extract the PlantVillage dataset."""
        try:
            # Create data directory if it doesn't exist
            self.data_dir.mkdir(parents=True, exist_ok=True)
            
            # Download the dataset
            logger.info("Downloading dataset...")
            response = requests.get(url, stream=True)
            zip_path = self.data_dir / "dataset.zip"
            
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Extract the dataset
            logger.info("Extracting dataset...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.data_dir)
            
            # Clean up
            os.remove(zip_path)
            logger.info("Dataset downloaded and extracted successfully")
            
        except Exception as e:
            logger.error(f"Error downloading dataset: {str(e)}")
            raise

    def prepare_data(self):
        """Prepare the dataset for training."""
        try:
            logger.info("Preparing dataset...")
            
            # Get all image directories
            image_paths = []
            labels = []
            
            # Walk through the data directory
            for class_dir in (self.data_dir / "PlantVillage").iterdir():
                if class_dir.is_dir():
                    self.class_names.append(class_dir.name)
                    for img_path in class_dir.glob("*.jpg"):
                        image_paths.append(str(img_path))
                        labels.append(len(self.class_names) - 1)
            
            # Convert to numpy arrays
            image_paths = np.array(image_paths)
            labels = np.array(labels)
            
            # Split the data
            train_paths, val_paths, train_labels, val_labels = train_test_split(
                image_paths, labels, test_size=0.2, random_state=42
            )
            
            return train_paths, val_paths, train_labels, val_labels
            
        except Exception as e:
            logger.error(f"Error preparing dataset: {str(e)}")
            raise

    def create_data_generator(self, image_paths, labels, batch_size=32):
        """Create a data generator for training/validation."""
        def generator():
            for img_path, label in zip(image_paths, labels):
                # Read and preprocess image
                img = tf.io.read_file(img_path)
                img = tf.image.decode_jpeg(img, channels=3)
                img = tf.image.resize(img, self.img_size)
                img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
                
                yield img, tf.one_hot(label, len(self.class_names))
        
        return tf.data.Dataset.from_generator(
            generator,
            output_signature=(
                tf.TensorSpec(shape=(*self.img_size, 3), dtype=tf.float32),
                tf.TensorSpec(shape=(len(self.class_names),), dtype=tf.float32)
            )
        ).batch(batch_size).prefetch(tf.data.AUTOTUNE)

    def build_model(self):
        """Build the CNN model."""
        # Use MobileNetV2 as base model
        base_model = tf.keras.applications.MobileNetV2(
            input_shape=(*self.img_size, 3),
            include_top=False,
            weights='imagenet'
        )
        
        # Freeze the base model
        base_model.trainable = False
        
        self.model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dropout(0.2),
            layers.Dense(512, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(len(self.class_names), activation='softmax')
        ])
        
        self.model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        logger.info("Model built successfully")
        return self.model

    def train(self, train_data, val_data, epochs=10):
        """Train the model."""
        if self.model is None:
            raise ValueError("Model not built. Call build_model() first.")
        
        # Add callbacks
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=3,
                restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.2,
                patience=2
            )
        ]
        
        # Train the model
        logger.info("Starting training...")
        history = self.model.fit(
            train_data,
            validation_data=val_data,
            epochs=epochs,
            callbacks=callbacks
        )
        
        return history

    def save_model(self, save_path='models/plant_disease_model.h5'):
        """Save the trained model."""
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Save the model
        self.model.save(save_path)
        
        # Save class names
        class_names_path = os.path.join(os.path.dirname(save_path), 'class_names.txt')
        with open(class_names_path, 'w') as f:
            f.write('\n'.join(self.class_names))
        
        logger.info(f"Model saved to {save_path}")

def main():
    # Initialize trainer
    trainer = PlantDiseaseTrainer()
    
    # Download dataset (you would need to provide the actual URL)
    # trainer.download_dataset("URL_TO_PLANTVILLAGE_DATASET")
    
    # Prepare data
    train_paths, val_paths, train_labels, val_labels = trainer.prepare_data()
    
    # Create data generators
    train_data = trainer.create_data_generator(train_paths, train_labels)
    val_data = trainer.create_data_generator(val_paths, val_labels)
    
    # Build and train model
    trainer.build_model()
    trainer.train(train_data, val_data)
    
    # Save model
    trainer.save_model()

if __name__ == "__main__":
    main() 