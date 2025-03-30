import os
import shutil
from sklearn.model_selection import train_test_split
from tqdm import tqdm

def create_split_datasets(source_dir, output_dir, val_size=0.15, test_size=0.15):
    """
    Split dataset into train, validation and test sets
    Args:
        source_dir: Directory containing the original dataset
        output_dir: Directory to save the split datasets
        val_size: Proportion of data to use for validation
        test_size: Proportion of data to use for testing
    """
    # Create output directories
    train_dir = os.path.join(output_dir, 'train')
    valid_dir = os.path.join(output_dir, 'valid')
    test_dir = os.path.join(output_dir, 'test')
    
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(valid_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    
    # Get all classes
    classes = []
    for d in os.listdir(source_dir):
        if os.path.isdir(os.path.join(source_dir, d)):
            classes.append(d)
    
    if not classes:
        raise ValueError(f"No class directories found in {source_dir}")
    
    for class_name in tqdm(classes, desc="Processing classes"):
        # Create class directories in train, valid, and test
        os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
        os.makedirs(os.path.join(valid_dir, class_name), exist_ok=True)
        os.makedirs(os.path.join(test_dir, class_name), exist_ok=True)
        
        # Get all images for this class
        class_dir = os.path.join(source_dir, class_name)
        images = [f for f in os.listdir(class_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if not images:
            print(f"Warning: No images found in {class_dir}")
            continue
        
        # Split into train, validation, and test
        train_imgs, test_imgs = train_test_split(images, test_size=test_size, random_state=42)
        train_imgs, valid_imgs = train_test_split(train_imgs, test_size=val_size/(1-test_size), random_state=42)
        
        # Copy images to respective directories
        for img in train_imgs:
            src = os.path.join(class_dir, img)
            dst = os.path.join(train_dir, class_name, img)
            shutil.copy2(src, dst)
        
        for img in valid_imgs:
            src = os.path.join(class_dir, img)
            dst = os.path.join(valid_dir, class_name, img)
            shutil.copy2(src, dst)
        
        for img in test_imgs:
            src = os.path.join(class_dir, img)
            dst = os.path.join(test_dir, class_name, img)
            shutil.copy2(src, dst)

def count_images(directory):
    """Count number of images in each split"""
    total = 0
    class_counts = {}
    
    for class_name in os.listdir(directory):
        class_path = os.path.join(directory, class_name)
        if os.path.isdir(class_path):
            count = len([f for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            class_counts[class_name] = count
            total += count
    
    return total, class_counts

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Prepare PlantVillage dataset splits")
    parser.add_argument(
        "--source_dir",
        type=str,
        default="/Users/ravitejakonanki/Downloads/archive/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/train",
        help="Source directory containing the original dataset"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="/Users/ravitejakonanki/Downloads/archive/Split_Dataset",
        help="Output directory for the split datasets"
    )
    parser.add_argument(
        "--val_size",
        type=float,
        default=0.15,
        help="Proportion of data to use for validation"
    )
    parser.add_argument(
        "--test_size",
        type=float,
        default=0.15,
        help="Proportion of data to use for testing"
    )
    
    args = parser.parse_args()
    
    # Create split datasets
    print(f"Source directory: {args.source_dir}")
    print(f"Output directory: {args.output_dir}")
    print("\nSplitting dataset...")
    create_split_datasets(args.source_dir, args.output_dir, args.val_size, args.test_size)
    
    # Count and display statistics
    print("\nDataset statistics:")
    for split in ['train', 'valid', 'test']:
        split_dir = os.path.join(args.output_dir, split)
        total, class_counts = count_images(split_dir)
        print(f"\n{split.capitalize()} set:")
        print(f"Total images: {total}")
        print("Images per class:")
        for class_name, count in sorted(class_counts.items()):
            print(f"  {class_name}: {count}") 