# import os
# import torch
# import torch.nn as nn
# import torch.optim as optim
# import torch.nn.functional as F
# from torchvision import datasets, transforms
# from torch.utils.data import DataLoader

# # Device
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# print(f'Using device: {device}')

# # Transform
# transform = transforms.Compose([
#     transforms.ToTensor(),
#     transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
# ])

# # Dataset + Loader
# train_dataset = datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
# train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

# # Model definition
# class CIFAR10CNN(nn.Module):
#     def __init__(self):
#         super(CIFAR10CNN, self).__init__()
#         self.conv1 = nn.Conv2d(3,32,3,padding=1)
#         self.conv2 = nn.Conv2d(32,64,3,padding=1)
#         self.conv3 = nn.Conv2d(64,128,3,padding=1)
#         self.pool = nn.MaxPool2d(2,2)
#         self.fc1 = nn.Linear(128*4*4,512)
#         self.fc2 = nn.Linear(512,10)
#         self.dropout = nn.Dropout(0.5)
#     def forward(self,x):
#         x = self.pool(F.relu(self.conv1(x)))
#         x = self.pool(F.relu(self.conv2(x)))
#         x = self.pool(F.relu(self.conv3(x)))
#         x = x.view(-1,128*4*4)
#         x = F.relu(self.fc1(x))
#         x = self.dropout(x)
#         x = self.fc2(x)
#         return x

# # Initialize model + optimizer
# model = CIFAR10CNN().to(device)
# criterion = nn.CrossEntropyLoss()
# optimizer = optim.Adam(model.parameters(), lr=0.001)

# # Auto‑resume if checkpoint exists
# checkpoint_path = "cifar10_checkpoint.pth"
# start_epoch = 0
# if os.path.exists(checkpoint_path):
#     print("Checkpoint found. Resuming training...")
#     checkpoint = torch.load(checkpoint_path)
#     model.load_state_dict(checkpoint['model_state_dict'])
#     optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
#     start_epoch = checkpoint['epoch']
#     print(f"Resumed from epoch {start_epoch}, loss={checkpoint['loss']:.4f}")
# else:
#     print("No checkpoint found. Starting fresh training...")

# # Training loop
# num_epochs = 10
# for epoch in range(start_epoch, num_epochs):
#     model.train()
#     running_loss, correct, total = 0.0, 0, 0
#     for images, labels in train_loader:
#         images, labels = images.to(device), labels.to(device)
#         outputs = model(images)
#         loss = criterion(outputs, labels)

#         optimizer.zero_grad()
#         loss.backward()
#         optimizer.step()

#         running_loss += loss.item()
#         _, predicted = torch.max(outputs.data, 1)
#         total += labels.size(0)
#         correct += (predicted == labels).sum().item()

#     epoch_loss = running_loss / len(train_loader)
#     epoch_acc = 100 * correct / total
#     print(f'Epoch {epoch+1}: Loss={epoch_loss:.4f}, Acc={epoch_acc:.2f}%')

#     # Save checkpoint after each epoch (overwrite)
#     torch.save({
#         'epoch': epoch+1,
#         'model_state_dict': model.state_dict(),
#         'optimizer_state_dict': optimizer.state_dict(),
#         'loss': epoch_loss,
#     }, checkpoint_path)

import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# Device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

# Transform
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
])

# Dataset + Loader
train_dataset = datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

# Model definition
class CIFAR10CNN(nn.Module):
    def __init__(self):
        super(CIFAR10CNN, self).__init__()
        self.conv1 = nn.Conv2d(3,32,3,padding=1)
        self.conv2 = nn.Conv2d(32,64,3,padding=1)
        self.conv3 = nn.Conv2d(64,128,3,padding=1)
        self.pool = nn.MaxPool2d(2,2)
        self.fc1 = nn.Linear(128*4*4,512)
        self.fc2 = nn.Linear(512,10)
        self.dropout = nn.Dropout(0.5)
    def forward(self,x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1,128*4*4)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

# Initialize model + optimizer
model = CIFAR10CNN().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Auto‑resume if checkpoint exists
checkpoint_path = "cifar10_checkpoint.pth"
start_epoch = 0
if os.path.exists(checkpoint_path):
    print("Checkpoint found. Resuming training...")
    checkpoint = torch.load(checkpoint_path, weights_only=True)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    start_epoch = checkpoint['epoch']
    print(f"Resumed from epoch {start_epoch}, loss={checkpoint['loss']:.4f}")
else:
    print("No checkpoint found. Starting fresh training...")

# Training loop
num_epochs = 100
train_losses, train_accs = [], []

print("Starting training...\n")

for epoch in range(start_epoch, num_epochs):
    model.train()
    running_loss, correct, total = 0.0, 0, 0
    
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
        
        # Print every 200 steps (old format)
        if (i + 1) % 200 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{len(train_loader)}], Loss: {loss.item():.4f}')
    
    # Epoch summary (old format)
    epoch_loss = running_loss / len(train_loader)
    epoch_acc = 100 * correct / total
    train_losses.append(epoch_loss)
    train_accs.append(epoch_acc)
    
    print(f'Epoch {epoch+1} Summary: Loss: {epoch_loss:.4f}, Accuracy: {epoch_acc:.2f}%\n')
    
    # Save checkpoint after each epoch (overwrite)
    torch.save({
        'epoch': epoch+1,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'loss': epoch_loss,
    }, checkpoint_path)