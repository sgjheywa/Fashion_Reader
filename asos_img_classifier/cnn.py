import torch
import torch.nn as nn
import torch.nn.functional as F
####8 cnn.py

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 3)
        self.conv1a = nn.Conv2d(6, 32, 3)
        self.conv1b = nn.Conv2d(32, 64, 3)
        self.conv1c = nn.Conv2d(64, 16, 1)
        self.conv1d = nn.Conv2d(16, 6, 1)

        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16*8*5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, len(clothing_types))

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv1a(x)))
        x = self.pool(F.relu(self.conv1b(x)))
        x = self.pool(F.relu(self.conv1c(x)))
        x = self.pool(F.relu(self.conv1d(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(1, 16*8*5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        # output = F.log_softmax(x, dim=1)
        return output
