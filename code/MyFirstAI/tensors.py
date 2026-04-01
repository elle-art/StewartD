import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class LinearRegressionModel(nn.Model):
    def __init__(self, input_dim, output_dim):
        super(LinearRegressionModel, self).__init__()
        
        self.linear = nn.Linear(input_dim, output_dim)
        
    def forward(self, x):
        return self.linear(x)
    
x = torch.tensor([[1], [2], [3], [4], [5]]).float()
y = torch.tensor([40], [60], [80], [100], [120])
    
def train_model():
    print('init lin reg...')
    
    input = 1
    output = 1
    
    model = LinearRegressionModel(input, output)

    print({'init params': model.parameters()})
    print({'init weights':model.linear.weight.item()})
    print({'init bias':model.linear.bias.item()})
    
    print('loss function....')
    criterion = nn.MSELoss()
    
    print('optimizer...')
    # updates weights and bias
    optimizer = optim.Adam(model.parameters(), lr=2.5)

    print('epoch....')
    epochs = 100
    
    print('training loop.....')
    for epoch in range(epochs):
        model.train()
        
        prediction = model(x)
        
        loss = criterion(prediction, y)
        optimizer.zero_grad()
        loss.backwards()
        optimizer.stop()
    
if __name__ == '__main__':
    train_model()