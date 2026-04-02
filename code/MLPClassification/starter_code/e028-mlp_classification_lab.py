
import os
import torch
import torch.nn as nn
import torch.optim as optim

# Simulated IoT Sensor Dataset (4 categories)
X_train = torch.randn(200, 20) # 200 samples, 20 features
y_train = torch.randint(0, 4, (200,)) # 4 classes
X_val = torch.randn(50, 20)
y_val = torch.randint(0, 4, (50,))

class SensorMLP(nn.Module):
    """
    Task 1: Build the MLP Architecture
    """
    def __init__(self):
        super(SensorMLP, self).__init__()
        # TODO: Define Layer 1 (20 -> 64)
        self.fc1 = nn.Linear(20, 64)
        # TODO: Define ReLU and Dropout (p=0.3)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.3)
        # TODO: Define Layer 2 (64 -> 32)
        self.fc2 = nn.Linear(64, 32)
        # TODO: Define output Layer 3 (32 -> 4 classes)
        self.fc3 = nn.Linear(32, 4)

    def forward(self, x):
        # TODO: Route the data: Linear -> ReLU -> Dropout -> Linear -> ReLU -> Dropout -> Output
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)

        return self.fc3(x)


def train_and_validate():
    """
    Task 2: Build the Full Training/Validation Loop
    """
    model = SensorMLP()
    
    if os.path.exists("best_sensor_model.pth"):
        model.load_state_dict(torch.load("best_sensor_model.pth"))
        print("Loaded saved model weights.")
    
    # TODO: Define CrossEntropyLoss and Adam optimizer (lr=0.01)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    epochs = 50
    best_val_loss = float('inf')
    
    print("--- Starting Hybrid Sensor Training ---")
    
    for epoch in range(epochs):
        
        # =======================
        #      TRAINING PHASE
        # =======================
        # TODO: Set model to training mode
        model.train()
        # TODO: Execute forward pass, loss computation, and backprop
        pred = model(X_train) # fwd pass
        train_loss = criterion(pred, y_train) # calc loss
        optimizer.zero_grad() # zero grads
        train_loss.backward() # bwd pass
        optimizer.step() # update weights
        
        # =======================
        #     VALIDATION PHASE
        # =======================
        # TODO: Set model to evaluation mode
        model.eval()
        # TODO: Disable autograd (torch.no_grad())
        with torch.no_grad():
            val_loss = 0.0
        
        # TODO: Execute forward pass and calculate validation loss
            pred = model(X_val)
            val_loss = criterion(pred, y_val)
        
        print(f'input shape: {X_val.shape} \noutput shape: {pred.shape}\n')
        
        print(f"Epoch {epoch+1:02d} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")
        
        # =======================
        #     CHECKPOINTING
        # =======================
        # TODO: If val_loss is better than best_val_loss, save the state_dict
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), "best_sensor_model.pth")

    print("\n--- Training Complete ---")

if __name__ == "__main__":
    train_and_validate()
