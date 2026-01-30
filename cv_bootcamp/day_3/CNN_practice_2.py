import torch
import torch.nn as nn
import torch.optim as optim 
import torch.nn.functional as F
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt 
import numpy as np

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

# PREPARE CIFAR-10 DATASET

# Data transformations
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# Load datasets
train_dataset = datasets.CIFAR10(root='./data', train=True,
                                download=True, transform=transform)
test_dataset = datasets.CIFAR10(root='./data', train=False,
                               download=True, transform=transform)

# Create data loaders
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

print(f'Training samples: {len(train_dataset)}')
print(f'Test samples: {len(test_dataset)}')

# Classes
classes = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

# Visualize some samples : shows 8 images 
# def show_images(images, labels, classes, num=8):
#     fig, axes = plt.subplots(1, num, figsize=(15, 2))
#     for i in range(num):
#         img = images[i].numpy().transpose(1, 2, 0)
#         img = img * 0.5 + 0.5  # Denormalize
#         axes[i].imshow(img)
#         axes[i].set_title(classes[labels[i]])
#         axes[i].axis('off')
#     plt.tight_layout()
#     plt.show()

# # Get a batch
# dataiter = iter(train_loader)
# images, labels = next(dataiter)
# show_images(images, labels, classes)

# visualise a lot of smaples : shows 64 images in 8x8 grid 

# def show_images_grid(images, labels, classes, rows=8, cols=8):
#     fig, axes = plt.subplots(rows, cols, figsize=(15, 15))
#     for i in range(rows * cols):
#         # Convert tensor to numpy image
#         img = images[i].numpy().transpose(1, 2, 0)
#         img = img * 0.5 + 0.5  # Denormalize (undo normalization)

#         # Plot image
#         r, c = divmod(i, cols)
#         axes[r, c].imshow(img)
#         axes[r, c].set_title(classes[labels[i]], fontsize=8)
#         axes[r, c].axis('off')

#     plt.tight_layout()
#     plt.show()

# # Get a batch
# dataiter = iter(train_loader)
# images, labels = next(dataiter)

# # Show 8x8 grid
# show_images_grid(images, labels, classes, rows=8, cols=8)

# actual model

class CIFAR10CNN(nn.Module):
    def __init__(self):
        super(CIFAR10CNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(128 * 4 * 4, 512)
        self.fc2 = nn.Linear(512, 10)
        self.dropout = nn.Dropout(0.5)
    
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1, 128 * 4 * 4)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

model = CIFAR10CNN().to(device)
print(model)
print(f'\nTotal parameters: {sum(p.numel() for p in model.parameters()):,}')


# overfitting one batch 

# # Take one batch
# test_images, test_labels = next(iter(train_loader))
# test_images, test_labels = test_images.to(device), test_labels.to(device)

# # Simple model for sanity check
# sanity_model = CIFAR10CNN().to(device)
# criterion = nn.CrossEntropyLoss()
# optimizer = optim.Adam(sanity_model.parameters(), lr=0.001)

# print("Sanity Check: Overfitting one batch...")
# print("Loss should decrease to near 0\n")

# for i in range(100):
#     outputs = sanity_model(test_images)
#     loss = criterion(outputs, test_labels)
    
#     optimizer.zero_grad()
#     loss.backward()
#     optimizer.step()
    
#     if i % 20 == 0:
#         _, predicted = torch.max(outputs, 1)
#         acc = (predicted == test_labels).sum().item() / test_labels.size(0)
#         print(f'Iteration {i:3d}: Loss = {loss.item():.4f}, Acc = {acc*100:.1f}%')

# print("\n✓ Sanity check passed! Model can learn." if loss.item() < 0.1 else "✗ Something wrong - loss should be near 0")

# Re-initialize model for actual training
model = CIFAR10CNN().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 10
train_losses = []
train_accs = []

print("Starting training...\n")

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for i, (images, labels) in enumerate(train_loader):
        images, labels = images.to(device), labels.to(device)
        
        # Forward
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # Backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        # Statistics
        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        
        if (i + 1) % 200 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{len(train_loader)}], Loss: {loss.item():.4f}')
    
    epoch_loss = running_loss / len(train_loader)
    epoch_acc = 100 * correct / total
    train_losses.append(epoch_loss)
    train_accs.append(epoch_acc)
    
    print(f'Epoch {epoch+1} Summary: Loss: {epoch_loss:.4f}, Accuracy: {epoch_acc:.2f}%\n')
  