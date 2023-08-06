import torch.nn as nn
import torch

# basic implementation of LeNet
# The input size 28x28 was not the same as the 32x32 image used in LeNet
class LeNet(nn.Module):
    def __init__(self, in_channels, num_classes):
        super(LeNet, self).__init__()
        self.conv1 = nn.Conv2d(in_channels = in_channels, out_channels = 6, kernel_size = 3, stride = 1, padding = 1)
        self.conv2 = nn.Conv2d(in_channels = 6, out_channels = 16, kernel_size = 5, stride = 1, padding = 0)
        self.conv3 = nn.Conv2d(in_channels = 16, out_channels = 120, kernel_size = 5, stride = 1, padding = 0)
        self.pool = nn.AvgPool2d(kernel_size = 2, stride = 2)
        self.fc1 = nn.Linear(120, 84)
        self.fc2 = nn.Linear(84, num_classes)
        
    def forward(self,x):
        # all the activation functions used in the original paper are tanh
        #INPUT -> C1: (conv1): Conv2d(1, 6, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        x = torch.tanh(self.conv1(x)) 
        #C1 -> S2: AvgPool2d(kernel_size=2, stride=2, padding=0)
        x = self.pool(x)    
        #S2 -> C3: (conv2): Conv2d(6, 16, kernel_size=(5, 5), stride=(1, 1))
        x = torch.tanh(self.conv2(x))  
        #C3 -> S4: AvgPool2d(kernel_size=2, stride=2, padding=0)
        x = self.pool(x)    
        #S4 -> C5 (16x5x5->120x1x1)(This conv layer plays the role of densing):
        #(conv3): Conv2d(16, 120, kernel_size=(5, 5), stride=(1, 1))
        x = torch.tanh(self.conv3(x))   
        x = x.reshape(x.shape[0], -1)  #unroll to 1d tensor
        #C5 -> F6: (fc1): Linear(in_features=120, out_features=84, bias=True)
        x = torch.tanh(self.fc1(x))   
        #F6 -> OUTPUT: (fc2): Linear(in_features=84, out_features=10, bias=True)
        """
        output layer

        The output layer is just a plain fc layer without activation function

        There is no need to add x = F.softmax(self.fc3(x)),
        because if you set loss = nn.CrossEntropyLoss(), 
        pytorch would perform softmax automatically
        """
        x = self.fc2(x) 
        return x