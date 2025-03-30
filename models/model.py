import torch
import torch.nn as nn
import torchvision.models as models
from typing import Dict, List, Tuple, Optional
import ssl

class PlantDiseaseModel(nn.Module):
    def __init__(self, num_classes: int, pretrained: bool = True):
        """
        Initialize the model
        Args:
            num_classes: Number of classes to predict
            pretrained: Whether to use pretrained weights
        """
        super().__init__()
        
        # Disable SSL verification for model download
        ssl._create_default_https_context = ssl._create_unverified_context
        
        try:
            # Try to load pretrained model
            self.model = models.resnet50(pretrained=pretrained)
        except Exception as e:
            print(f"Warning: Could not load pretrained weights: {e}")
            print("Initializing model with random weights...")
            self.model = models.resnet50(pretrained=False)
        
        # Modify the final layer for our number of classes
        num_features = self.model.fc.in_features
        self.model.fc = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )
        
        # Loss function
        self.criterion = nn.CrossEntropyLoss()
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass"""
        return self.model(x)
    
    def training_step(self, batch: Tuple[torch.Tensor, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """
        Training step
        Args:
            batch: Tuple of (images, labels)
        Returns:
            Dictionary containing loss and accuracy
        """
        images, labels = batch
        outputs = self(images)
        loss = self.criterion(outputs, labels)
        
        # Calculate accuracy
        _, predicted = outputs.max(1)
        accuracy = (predicted == labels).float().mean()
        
        return {
            'loss': loss,
            'accuracy': accuracy
        }
    
    def validation_step(self, batch: Tuple[torch.Tensor, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """
        Validation step
        Args:
            batch: Tuple of (images, labels)
        Returns:
            Dictionary containing loss and accuracy
        """
        images, labels = batch
        outputs = self(images)
        loss = self.criterion(outputs, labels)
        
        # Calculate accuracy
        _, predicted = outputs.max(1)
        accuracy = (predicted == labels).float().mean()
        
        return {
            'loss': loss,
            'accuracy': accuracy
        }
    
    def predict(self, image: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Make prediction for a single image
        Args:
            image: Input image tensor
        Returns:
            Tuple of (predictions, probabilities)
        """
        outputs = self(image)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        predictions = torch.argmax(probabilities, dim=1)
        return predictions, probabilities
    
    def configure_optimizers(self, lr: float = 0.001) -> torch.optim.Optimizer:
        """Configure model optimizer"""
        return torch.optim.Adam(self.parameters(), lr=lr) 