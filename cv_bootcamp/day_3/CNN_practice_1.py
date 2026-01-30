import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt

# print(f'PyTorch version: {torch.__version__}')
# print(f'CUDA available: {torch.cuda.is_available()}')
# print(f'matplotlib version: {matplotlib.__version__}')

# # Single convolutional layer
# conv = nn.Conv2d(
#     in_channels=3,      # RGB input
#     out_channels=32,    # 32 filters
#     kernel_size=3,      # 3x3 filters
#     stride=1,           # Move 1 pixel at a time
#     padding=1           # Pad to keep size same
# )

# # Input: batch of RGB images
# x = torch.randn(16, 3, 32, 32)  # (batch, channels, height, width)
# output = conv(x)

# print(f'Input shape: {x.shape}')
# print(f'Output shape: {output.shape}')  # (16, 32, 32, 32) - 32 feature maps
# print(f'Number of learnable parameters: {sum(p.numel() for p in conv.parameters()):,}')

# # Demonstrate shrinking without padding
# x = torch.randn(1, 3, 32, 32)

# # No padding
# conv_no_pad = nn.Conv2d(3, 3, kernel_size=3, padding=0)
# out_no_pad = conv_no_pad(x)

# # With padding
# conv_with_pad = nn.Conv2d(3, 3, kernel_size=3, padding=1)
# out_with_pad = conv_with_pad(x)

# print("Input shape:", x.shape)
# print("Output without padding:", out_no_pad.shape)  # Shrinks to 30x30
# print("Output with padding=1:", out_with_pad.shape)  # Stays 32x32

# # After 5 layers without padding
# print("\nAfter 5 conv layers without padding:")
# temp = x
# for i in range(5):
#     temp = conv_no_pad(temp)
#     print(f"  After layer {i+1}: {temp.shape[2]}x{temp.shape[3]}")

# # we lose parts of the image with successive layers


# # activation funcitons, used to create non linearity to better classify inputs, whether or not to fire a neuron 

# # ReLU: max(0, x) - most common
# # if the input is -vem give 0 else, give the number itself

# relu = nn.ReLU()
# x = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0])
# print(f'Input: {x}')
# print(f'ReLU output: {relu(x)}')  # Negative values become 0

# # Visualize ReLU
# x_range = torch.linspace(-3, 3, 100)
# y_relu = relu(x_range)

# plt.figure(figsize=(8, 4))
# plt.plot(x_range.numpy(), y_relu.numpy(), linewidth=2)
# plt.grid(True, alpha=0.3)
# plt.xlabel('Input')
# plt.ylabel('Output')
# plt.title('ReLU Activation Function')
# plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
# plt.axvline(x=0, color='k', linestyle='--', alpha=0.3)
# plt.show()

# # Other activation functions
# sigmoid = nn.Sigmoid()
# tanh = nn.Tanh()
# leaky_relu = nn.LeakyReLU(0.1)

# x = torch.tensor([-1.0, 0.0, 1.0])
# print(f'Input: {x}')
# print(f'Sigmoid: {sigmoid(x)}')
# print(f'Tanh: {tanh(x)}')
# print(f'Leaky ReLU: {leaky_relu(x)}')

# pooling layers
# downsampling feature maps to reduce computation, make features robust to small shifts and increase recepitve field

# Max pooling: take maximum value in each region
# max_pool = nn.MaxPool2d(kernel_size=2, stride=2)
# x = torch.randn(1, 32, 32, 32)
# output = max_pool(x)

# print(f'Input shape: {x.shape}')
# print(f'Output shape: {output.shape}')  # Halved dimensions

# # Demonstrate max pooling visually
# sample = torch.tensor([[
#     [1, 2, 3, 4],
#     [5, 6, 7, 8],
#     [9, 10, 11, 12],
#     [13, 14, 15, 16]
# ]], dtype=torch.float32).unsqueeze(0)  # Add batch and channel dims

# pooled = max_pool(sample)
# print("\nBefore pooling:")
# print(sample.squeeze())
# print("\nAfter 2x2 max pooling:")
# print(pooled.squeeze())
# print("\nNotice: Each 2x2 region → maximum value")
     
# # Average pooling
# avg_pool = nn.AvgPool2d(kernel_size=2, stride=2)
# output_avg = avg_pool(x)
# print(f'Avg pool output: {output_avg.shape}')

# # Compare max vs avg pooling
# pooled_avg = avg_pool(sample)
# print("\nMax pooling result:")
# print(pooled.squeeze())
# print("\nAverage pooling result:")
# print(pooled_avg.squeeze())

# class SimpleCNN(nn.Module):
#     def __init__(self, num_classes=10):
#         super(SimpleCNN, self).__init__()
        
#         # Convolutional layers
#         self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
#         self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
#         self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        
#         # Pooling layer
#         self.pool = nn.MaxPool2d(2, 2)
        
#         # Fully connected layers
#         self.fc1 = nn.Linear(128 * 4 * 4, 512)
#         self.fc2 = nn.Linear(512, num_classes)
        
#         # Dropout for regularization              dropout means to ignore the responses of a certain set of neurons
#                                                   so that different features are recognized and memorisation of a particular feature is avoided
#         self.dropout = nn.Dropout(0.5)
    
#     def forward(self, x):
#         # in each block, we use the relu activation function on the output of the corresponding convolutional layer, then pool it(max pool 2d)
#         # as input for the next layer 
          
#         # Block 1: Conv -> ReLU -> Pool
#         x = self.pool(F.relu(self.conv1(x)))  # 32x32 -> 16x16
        
#         # Block 2
#         x = self.pool(F.relu(self.conv2(x)))  # 16x16 -> 8x8
        
#         # Block 3
#         x = self.pool(F.relu(self.conv3(x)))  # 8x8 -> 4x4
        
#         # Flatten: Convert 3D features to 1D
#         x = x.view(-1, 128 * 4 * 4)
        
#         # Fully connected layers
#         x = F.relu(self.fc1(x))
#         x = self.dropout(x)
#         x = self.fc2(x)
        
#         return x

# # Instantiate and test
# model = SimpleCNN(num_classes=10)
# x = torch.randn(4, 3, 32, 32)  # Batch of 4 images
# output = model(x)

# print(f'Model output shape: {output.shape}')  # (4, 10) - 10 class scores
# print(f'\nModel architecture:')
# print(model)

# # counting paramters
# total_params = sum(p.numel() for p in model.parameters())
# trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

# print(f'Total parameters: {total_params:,}')
# print(f'Trainable parameters: {trainable_params:,}')

# # Layer-wise parameter count
# print("\nParameters per layer:")
# for name, param in model.named_parameters():
#     print(f'{name:20s}: {param.numel():>8,} parameters')
     
class VerboseCNN(nn.Module):
    """CNN that prints shape after each operation"""
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 8 * 8, 10)
    
    def forward(self, x):
        print(f"Input: {x.shape}")
        
        x = F.relu(self.conv1(x))
        print(f"After conv1 + ReLU: {x.shape}")
        
        x = self.pool(x)
        print(f"After pool: {x.shape}")
        
        x = F.relu(self.conv2(x))
        print(f"After conv2 + ReLU: {x.shape}")
        
        x = self.pool(x)
        print(f"After pool: {x.shape}")
        
        x = x.view(x.size(0), -1)
        print(f"After flatten: {x.shape}")
        
        x = self.fc1(x)
        print(f"After fc: {x.shape}")
        
        return x

verbose_model = VerboseCNN()
test_input = torch.randn(2, 3, 32, 32)
_ = verbose_model(test_input)