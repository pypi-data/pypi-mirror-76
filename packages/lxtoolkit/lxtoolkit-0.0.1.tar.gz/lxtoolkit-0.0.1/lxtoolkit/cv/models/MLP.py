import torch.nn as nn
"""
 This is a very basic Multilayer perceptron(used for MNIST dataset) example
 You can modify this basic model if you like

print(model) on  MINST:
MLP(
  (fc1): Linear(in_features=784, out_features=120, bias=True)
  (fc2): Linear(in_features=120, out_features=80, bias=True)
  (fc3): Linear(in_features=80, out_features=10, bias=True)
  (relu): ReLU(inplace=True)
)
!!!fc1 and fc2 have activation function ReLU, but fc3 hasn't(explained below)
"""

class MLP(nn.Module):
    # input_size -> 28 x 28 x 1 = 784 (grayscale image -> height x width x 1)
    def __init__(self, input_size, num_classes):
        super().__init__()
                
        self.fc1 = nn.Linear(input_size, 120)
        self.fc2 = nn.Linear(120, 80)
        self.fc3 = nn.Linear(80, num_classes)
        self.relu = nn.ReLU(inplace = True)

    def forward(self, x): 
        # x.shape == (batch_size, 28, 28)
        batch_size = x.shape[0]
        # matrix -> vector; the x.view is inplace
        # vector.shape == (batch_size, 784)
        x = x.view(batch_size, -1)
        # 2 hidden layers
        # (batch_size, 784) -> (batch_size, 120)
        x = self.relu(self.fc1(x))
        # (batch_size, 120) -> (batch_size, 84)
        x = self.relu(self.fc2(x))
        """
        output layer

        The output layer is just a plain fc layer without activation function

        There is no need to add x = F.softmax(self.fc3(x)),
        because if you set loss = nn.CrossEntropyLoss(), 
        pytorch would perform softmax automatically
        """
        #(batch_size, 84) -> (batch_size, 10)
        x = self.fc3(x)
        # now, x == predicted scores for classes
        return x