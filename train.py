import os
import argparse
import torch
import json
from models.data_loader import create_data_loaders, get_class_mapping
from models.model import PlantDiseaseModel
from models.trainer import PlantDiseaseTrainer

def main():
    parser = argparse.ArgumentParser(description="Train Plant Disease Detection Model")
    parser.add_argument(
        "--data_dir",
        type=str,
        default="/Users/ravitejakonanki/Downloads/archive/Split_Dataset",
        help="Directory containing train, valid, and test folders"
    )
    parser.add_argument(
        "--save_dir",
        type=str,
        default="checkpoints",
        help="Directory to save model checkpoints"
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=32,
        help="Batch size for training"
    )
    parser.add_argument(
        "--num_epochs",
        type=int,
        default=10,
        help="Number of epochs to train"
    )
    parser.add_argument(
        "--num_workers",
        type=int,
        default=4,
        help="Number of workers for data loading"
    )
    parser.add_argument(
        "--learning_rate",
        type=float,
        default=0.001,
        help="Learning rate for training"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="Device to use for training"
    )
    
    args = parser.parse_args()
    
    # Create save directory
    os.makedirs(args.save_dir, exist_ok=True)
    
    # Create data loaders
    print("Loading datasets...")
    train_loader, valid_loader, test_loader, classes = create_data_loaders(
        args.data_dir,
        batch_size=args.batch_size,
        num_workers=args.num_workers
    )
    
    # Create class mapping
    class_mapping = get_class_mapping(classes)
    
    # Save class mapping
    mapping_path = os.path.join(args.save_dir, "class_mapping.json")
    with open(mapping_path, "w") as f:
        json.dump(class_mapping, f, indent=4)
    print(f"Saved class mapping to {mapping_path}")
    
    # Create model
    print("Creating model...")
    model = PlantDiseaseModel(num_classes=len(classes))
    
    # Create trainer
    print("Initializing trainer...")
    trainer = PlantDiseaseTrainer(
        model=model,
        train_loader=train_loader,
        valid_loader=valid_loader,
        device=args.device,
        learning_rate=args.learning_rate
    )
    
    # Train model
    print("Starting training...")
    trainer.train(
        num_epochs=args.num_epochs,
        save_dir=args.save_dir
    )
    
    # Evaluate on test set
    print("\nEvaluating on test set...")
    test_loss, test_acc = trainer.validate(test_loader)
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_acc:.2f}%")

if __name__ == "__main__":
    main() 