import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
import seaborn as sns


def unfreeze_last_n_layers(model, n=1):
    """Unfreeze last n residual blocks"""
    layers = [model.layer4, model.layer3, model.layer2, model.layer1]
    for i in range(n):
        for param in layers[i].parameters():
            param.requires_grad = True
    return model


# Paths
model_path = "best_model_1.pth"

# Data augmentation for training
train_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.RandomCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2,
                           saturation=0.2, hue=0.1),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# No augmentation for validation / test
val_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# Load datasets
train_dataset = datasets.ImageFolder('data/train', transform=train_transforms)
val_dataset = datasets.ImageFolder('data/val', transform=val_transforms)
test_dataset = datasets.ImageFolder('data/test', transform=val_transforms)

# Create data loaders (set num_workers=0 for Windows safety)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=0)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=0)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=0)

print(f'Training samples: {len(train_dataset)}')
print(f'Validation samples: {len(val_dataset)}')
print(f'Test samples: {len(test_dataset)}')

# Load pretrained ResNet18
model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)

# Freeze all layers
for param in model.parameters():
    param.requires_grad = False

# unfreezing a few layers for fine tuning 
model = unfreeze_last_n_layers(model,2)
# Replace final layer for binary classification
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, 2)

# Move to GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

print(f'Using device: {device}')
print(f'Training only final layer with {model.fc.in_features} input features mapped to 2 outputs')

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
# optimizer = optim.Adam(model.fc.parameters(), lr=0.001)

optimizer = optim.Adam([
    {'params': model.layer4.parameters(), 'lr': 1e-4},
    {'params': model.layer3.parameters(), 'lr': 1e-5},
    {'params': model.fc.parameters(), 'lr': 1e-3}
])

# Learning rate scheduler
scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode='min', patience=3, factor=0.5
)

# Training tracking
train_losses, val_losses = [], []
train_accs, val_accs = [], []
best_val_acc = 0.0
num_epochs = 5

# --- Main guard for Windows multiprocessing ---
if __name__ == "__main__":

    # Check if model already exists
    if os.path.exists(model_path):
        print("Found saved model, loading instead of training...")
        model.load_state_dict(torch.load(model_path))
        model.eval()
    else:
        print("No saved model found, starting training...")
        for epoch in range(num_epochs):
            # Training phase
            model.train()
            running_loss, correct, total = 0.0, 0, 0

            for images, labels in train_loader:
                images, labels = images.to(device), labels.to(device)

                outputs = model(images)
                loss = criterion(outputs, labels)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                running_loss += loss.item() * images.size(0)
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()

            epoch_loss = running_loss / len(train_dataset)
            epoch_acc = correct / total
            train_losses.append(epoch_loss)
            train_accs.append(100 * epoch_acc)

            # Validation phase
            model.eval()
            val_running_loss, val_correct, val_total = 0.0, 0, 0
            with torch.no_grad():
                for images, labels in val_loader:
                    images, labels = images.to(device), labels.to(device)
                    outputs = model(images)
                    loss = criterion(outputs, labels)

                    val_running_loss += loss.item()
                    _, predicted = torch.max(outputs.data, 1)
                    val_total += labels.size(0)
                    val_correct += (predicted == labels).sum().item()

            val_loss = val_running_loss / len(val_loader)
            val_acc = 100 * val_correct / val_total
            val_losses.append(val_loss)
            val_accs.append(val_acc)

            scheduler.step(val_loss)

            if val_acc > best_val_acc:
                best_val_acc = val_acc
                torch.save(model.state_dict(), model_path)
                print(f'Saved best model with val_acc: {val_acc:.2f}%')

            print(f'Epoch [{epoch+1}/{num_epochs}]')
            print(f'Train Loss: {epoch_loss:.4f}, Train Acc: {epoch_acc*100:.2f}%')
            print(f'Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%\n')

        # Load best model after training
        model.load_state_dict(torch.load(model_path,weights_only = True))
        model.eval()

    # --- Testing phase ---
    correct, total = 0, 0
    all_preds, all_labels = [], []

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)

            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    test_accuracy = 100 * correct / total
    print(f'Test Accuracy: {test_accuracy:.2f}%')

    # --- Plot training curves ---
    if train_losses and val_losses:  # Only plot if training was run
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        ax1.plot(train_losses, label='Train Loss')
        ax1.plot(val_losses, label='Val Loss')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss')
        ax1.set_title('Training and Validation Loss')
        ax1.legend()

        ax2.plot(train_accs, label='Train Acc')
        ax2.plot(val_accs, label='Val Acc')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy (%)')
        ax2.set_title('Training and Validation Accuracy')
        ax2.legend()

        plt.tight_layout()
        plt.savefig('training_curves.png')
        plt.show()

    # --- Confusion matrix ---
    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.savefig('confusion_matrix.png')
    plt.show()

    # Collect some correct and incorrect examples
    correct_images, wrong_images = [], []

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)

            for img, label, pred in zip(images, labels, predicted):
                if len(correct_images) < 10 and pred == label:
                    correct_images.append((img.cpu(), label.cpu(), pred.cpu()))
                elif len(wrong_images) < 10 and pred != label:
                    wrong_images.append((img.cpu(), label.cpu(), pred.cpu()))

            # Stop once we have 10 correct + 10 wrong
            if len(correct_images) >= 10 and len(wrong_images) >= 10:
                break

    # Helper to unnormalize for display
    def imshow(img_tensor):
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        img = img_tensor.permute(1, 2, 0).numpy()
        img = std * img + mean
        img = np.clip(img, 0, 1)
        return img

    # Plot 20 images in 4x5 grid
    fig, axes = plt.subplots(4, 5, figsize=(15, 10))
    axes = axes.flatten()

    # First 10 = correct
    for i, (img, label, pred) in enumerate(correct_images):
        axes[i].imshow(imshow(img))
        axes[i].set_title(f"✓ Label:{label.item()} Pred:{pred.item()}", color="green")
        axes[i].axis("off")

    # Next 10 = wrong
    for i, (img, label, pred) in enumerate(wrong_images, start=10):
        axes[i].imshow(imshow(img))
        axes[i].set_title(f"✗ Label:{label.item()} Pred:{pred.item()}", color="red")
        axes[i].axis("off")

    plt.tight_layout()
    plt.show()