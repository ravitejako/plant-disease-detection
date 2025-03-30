import torch
import torch.nn as nn
from typing import Dict, List, Tuple, Optional
from tqdm import tqdm
import numpy as np
import json
import os
from datetime import datetime

class PlantDiseaseTrainer:
    def __init__(
        self,
        model: nn.Module,
        train_loader: torch.utils.data.DataLoader,
        valid_loader: Optional[torch.utils.data.DataLoader] = None,
        device: str = 'cuda' if torch.cuda.is_available() else 'cpu',
        learning_rate: float = 0.001
    ):
        """
        Initialize the trainer
        Args:
            model: The model to train
            train_loader: DataLoader for training data
            valid_loader: DataLoader for validation data
            device: Device to use for training
            learning_rate: Initial learning rate
        """
        self.model = model.to(device)
        self.train_loader = train_loader
        self.valid_loader = valid_loader
        self.device = device
        self.learning_rate = learning_rate
        
        # Initialize optimizer and scheduler
        self.optimizer = self._get_optimizer()
        self.scheduler = self._get_scheduler()
        self.criterion = nn.CrossEntropyLoss()
        
        # Initialize history
        self.history = {
            'train_loss': [],
            'train_acc': [],
            'valid_loss': [],
            'valid_acc': []
        }
        
        # Early stopping
        self.best_valid_acc = 0.0
        self.patience = 5
        self.patience_counter = 0
    
    def _get_optimizer(self):
        """Get the optimizer"""
        return torch.optim.AdamW(
            self.model.parameters(),
            lr=self.learning_rate,
            weight_decay=0.01
        )
    
    def _get_scheduler(self):
        """Get the learning rate scheduler"""
        return torch.optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer,
            mode='max',
            factor=0.5,
            patience=2,
            verbose=True
        )
    
    def train_epoch(self) -> Tuple[float, float]:
        """Train for one epoch"""
        self.model.train()
        total_loss = 0.0
        total_acc = 0.0
        
        progress_bar = tqdm(self.train_loader, desc='Training')
        for batch in progress_bar:
            # Move batch to device
            images, labels = [x.to(self.device) for x in batch]
            
            # Zero gradients
            self.optimizer.zero_grad()
            
            # Forward pass
            results = self.model.training_step((images, labels))
            loss = results['loss']
            accuracy = results['accuracy']
            
            # Backward pass
            loss.backward()
            self.optimizer.step()
            
            # Update metrics
            total_loss += loss.item()
            total_acc += accuracy.item()
            
            # Update progress bar
            progress_bar.set_postfix({
                'loss': f'{loss.item():.4f}',
                'acc': f'{accuracy.item():.4f}'
            })
        
        avg_loss = total_loss / len(self.train_loader)
        avg_acc = total_acc / len(self.train_loader)
        return avg_loss, avg_acc
    
    def validate(self) -> Tuple[float, float]:
        """Validate the model"""
        if not self.valid_loader:
            return 0.0, 0.0
        
        self.model.eval()
        total_loss = 0.0
        total_acc = 0.0
        
        with torch.no_grad():
            progress_bar = tqdm(self.valid_loader, desc='Validating')
            for batch in progress_bar:
                # Move batch to device
                images, labels = [x.to(self.device) for x in batch]
                
                # Forward pass
                results = self.model.validation_step((images, labels))
                loss = results['loss']
                accuracy = results['accuracy']
                
                # Update metrics
                total_loss += loss.item()
                total_acc += accuracy.item()
                
                # Update progress bar
                progress_bar.set_postfix({
                    'loss': f'{loss.item():.4f}',
                    'acc': f'{accuracy.item():.4f}'
                })
        
        avg_loss = total_loss / len(self.valid_loader)
        avg_acc = total_acc / len(self.valid_loader)
        return avg_loss, avg_acc
    
    def save_checkpoint(self, epoch, save_dir):
        """Save a checkpoint"""
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'history': self.history,
            'best_valid_acc': self.best_valid_acc
        }
        
        # Save best model
        if self.best_valid_acc > 0:
            best_model_path = os.path.join(save_dir, 'best_model.pth')
            torch.save(checkpoint, best_model_path)
        
        # Save latest model
        latest_model_path = os.path.join(save_dir, 'latest_model.pth')
        torch.save(checkpoint, latest_model_path)
        
        # Save training history
        history_path = os.path.join(save_dir, 'training_history.json')
        with open(history_path, 'w') as f:
            json.dump(self.history, f, indent=4)
    
    def train(self, num_epochs: int, save_dir: str = 'checkpoints') -> Dict:
        """Train the model for specified number of epochs"""
        os.makedirs(save_dir, exist_ok=True)
        print(f"Training on {self.device}")
        print(f"Initial learning rate: {self.learning_rate}")
        
        for epoch in range(num_epochs):
            print(f'\nEpoch {epoch+1}/{num_epochs}')
            
            # Training phase
            train_loss, train_acc = self.train_epoch()
            self.history['train_loss'].append(train_loss)
            self.history['train_acc'].append(train_acc)
            
            # Validation phase
            if self.valid_loader:
                valid_loss, valid_acc = self.validate()
                self.history['valid_loss'].append(valid_loss)
                self.history['valid_acc'].append(valid_acc)
                
                # Update learning rate
                self.scheduler.step(valid_acc)
                
                # Save best model
                if valid_acc > self.best_valid_acc:
                    self.best_valid_acc = valid_acc
                    self.patience_counter = 0
                    self.save_checkpoint(epoch, save_dir)
                else:
                    self.patience_counter += 1
                    if self.patience_counter >= self.patience:
                        print(f"\nEarly stopping triggered after {epoch + 1} epochs")
                        break
            
            # Print epoch results
            print(f'Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}')
            if self.valid_loader:
                print(f'Valid Loss: {valid_loss:.4f}, Valid Acc: {valid_acc:.4f}')
        
        # Save final checkpoint
        self.save_checkpoint(num_epochs, save_dir)
        print("\nTraining completed!")
        
        return self.history
    
    def predict(self, image_tensor: torch.Tensor) -> Tuple[int, float]:
        """Make prediction for a single image"""
        self.model.eval()
        image_tensor = image_tensor.to(self.device)
        
        with torch.no_grad():
            predictions, probabilities = self.model.predict(image_tensor)
            
            # Get the predicted class and its probability
            pred_class = predictions[0].item()
            pred_prob = probabilities[0][pred_class].item()
        
        return pred_class, pred_prob 