import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import json

class PlantDiseaseDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        """
        Args:
            root_dir (string): Directory with all the images
            transform (callable, optional): Optional transform to be applied on an image
        """
        self.root_dir = root_dir
        self.transform = transform
        self.classes = sorted([d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))])
        self.class_to_idx = {cls: idx for idx, cls in enumerate(self.classes)}
        
        self.images = []
        self.labels = []
        
        # Load all image paths and labels
        for class_name in self.classes:
            class_dir = os.path.join(root_dir, class_name)
            for img_name in os.listdir(class_dir):
                if img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    self.images.append(os.path.join(class_dir, img_name))
                    self.labels.append(self.class_to_idx[class_name])
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img_path = self.images[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label
    
    def get_class_name(self, idx):
        """Get the class name for a given index"""
        return self.classes[idx]

def get_data_transforms():
    """Get data transforms for training and validation"""
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    return train_transform, val_transform

def create_data_loaders(data_dir, batch_size=32, num_workers=4):
    """
    Create data loaders for train, validation and test sets
    Args:
        data_dir (string): Root directory containing train, valid, and test folders
        batch_size (int): Batch size for the data loaders
        num_workers (int): Number of workers for data loading
    Returns:
        tuple: (train_loader, valid_loader, test_loader)
    """
    train_transform, val_transform = get_data_transforms()
    
    # Create datasets
    train_dataset = PlantDiseaseDataset(
        os.path.join(data_dir, 'train'),
        transform=train_transform
    )
    
    valid_dataset = PlantDiseaseDataset(
        os.path.join(data_dir, 'valid'),
        transform=val_transform
    )
    
    test_dataset = PlantDiseaseDataset(
        os.path.join(data_dir, 'test'),
        transform=val_transform
    )
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )
    
    valid_loader = DataLoader(
        valid_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    return train_loader, valid_loader, test_loader, train_dataset.classes

def process_single_image(image_path, transform=None):
    """
    Process a single image for prediction
    Args:
        image_path (string): Path to the image file
        transform (callable, optional): Transform to be applied on the image
    Returns:
        tensor: Processed image tensor
    """
    if transform is None:
        _, val_transform = get_data_transforms()
        transform = val_transform
    
    image = Image.open(image_path).convert('RGB')
    return transform(image).unsqueeze(0)

def get_class_mapping(dataset_classes):
    """
    Create a mapping between class indices and class names
    Args:
        dataset_classes (list): List of class names
    Returns:
        dict: Mapping between indices and class names
    """
    return {idx: name for idx, name in enumerate(dataset_classes)} 