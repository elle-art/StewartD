import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from pathlib import Path

# =============================================================================
# Set this to the path of any JPEG or PNG image on your machine.
# Leave it as None to fall back to a randomly generated dummy image.
#
# Example:  IMAGE_PATH = "C:/Users/you/Pictures/cat.jpg"
# =============================================================================
IMAGE_PATH = r'C:\Users\dnico\Documents\RevatureAIATraining\StewartD\code\w7-notes\img_0_403.jpg'


# --- CNN Block Definition ---
class SimpleCNNBlock(nn.Module):
    def __init__(self):
        super().__init__()
        # 3 input channels (RGB), 16 output feature maps, 3x3 filter
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=1, padding=1)
        self.relu = nn.ReLU()
        # MaxPool halves the spatial dimensions (224 → 112)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

    def forward(self, x):
        # x shape in:  [Batch, 3,  224, 224]
        x = self.conv1(x)   # → [Batch, 16, 224, 224]
        x = self.relu(x)
        x = self.pool(x)    # → [Batch, 16, 112, 112]
        return x


# --- Load image or fall back to a dummy tensor ---
if IMAGE_PATH:
    from PIL import Image
    from torchvision import transforms

    # torchvision.transforms preprocesses a PIL image into a normalised float tensor.
    # Resize ensures the image matches the 224x224 input size CNNs expect.
    # ToTensor converts PIL [H, W, C] uint8 (0–255) → torch [C, H, W] float32 (0.0–1.0)
    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

    raw_image = Image.open(IMAGE_PATH).convert("RGB")  # Force 3-channel RGB
    input_tensor = preprocess(raw_image).unsqueeze(0)  # Add batch dim: [1, 3, 224, 224]
    source_label = f"Your image: {Path(IMAGE_PATH).name}"
    print(f"Loaded:  {IMAGE_PATH}")
else:
    input_tensor = torch.randn(1, 3, 224, 224)
    source_label = "Source: random noise (no IMAGE_PATH set)"
    print("IMAGE_PATH is None — using a random dummy tensor.")
    print("Set IMAGE_PATH at the top of this file to use your own image.\n")

# --- Run the CNN block ---
model = SimpleCNNBlock()
model.eval()  # Disable any training-specific behaviour (good inference habit)

with torch.no_grad():  # No gradient tracking needed for visualisation
    feature_maps = model(input_tensor)

print(f"Input tensor shape  : {input_tensor.shape}  [batch, channels, H, W]")
print(f"Feature maps shape  : {feature_maps.shape}  [batch, filters, H, W]")
print(f"  → {feature_maps.shape[1]} filters, each {feature_maps.shape[2]}×{feature_maps.shape[3]} pixels")

# --- Visualise: original image + first 4 feature maps ---
fig, axes = plt.subplots(1, 5, figsize=(18, 3))

# Panel 0 — original input image
# Permute from [C, H, W] → [H, W, C] so matplotlib can display it as RGB
# clamp(0, 1) prevents any colour values from going out of range
original_display = input_tensor[0].permute(1, 2, 0).clamp(0, 1)
axes[0].imshow(original_display)
axes[0].set_title("Original Input", fontweight='bold')
axes[0].axis('off')

# Panels 1–4 — the first 4 of the 16 output feature maps
# Each map shows which parts of the image activated a specific learned filter.
# Bright areas = strong response; dark areas = weak response.
for i in range(4):
    # .detach() removes the tensor from the autograd graph before numpy conversion
    axes[i + 1].imshow(feature_maps[0, i].detach(), cmap='viridis')
    axes[i + 1].set_title(f'Filter {i + 1} response')
    axes[i + 1].axis('off')

plt.suptitle(
    f'Feature maps after Conv2d → ReLU → MaxPool\n{source_label}',
    fontsize=12
)
plt.tight_layout()
plt.show()
