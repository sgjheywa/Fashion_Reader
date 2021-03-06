
####5 demo.py
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision

import preprocessing as pre
import cnn
import model


df = pd.read_csv("training_data/labels.csv")
print(df.head())

clothing_labels = ['hoodies','shorts']


sample = df.loc[0]
print("filename: ",sample[1], " label: ",sample[2])

npimg = Image.open(sample[1])
plt.imshow(npimg)
#plt.show()
print("label:", clothing_labels.index(sample[2]), sample[2])

split_point = int(len(df)*0.9)
train_df = df.loc[0:split_point-1]
test_df = df.loc[split_point:]


train_images, train_labels = pre.build_torch_dataset(train_df, 0, clothing_labels)   
test_images, test_labels = pre.build_torch_dataset(test_df, 0, clothing_labels) 

print(len(train_images), len(test_images))
print(train_images[0].shape)
       
batch_train_images, batch_train_labels = pre.batch_up(train_images, train_labels, 4)

# net = cnn.Net()

if torch.cuda.is_available():
    device = 'cuda'
else:
    device = 'cpu'

net = torchvision.models.MobileNetV2().to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.0001, momentum=0.9)
model = model.Model(net, criterion, optimizer, device)

model.train(batch_train_images, batch_train_labels, epoch=5)

model.test(test_images, test_labels)

PATH = 'saved_models/asosnet.pth'
torch.save(net.state_dict(), PATH)

# to do
# verify urls for dupes
# dynamic url amounts when readig them in
# pos tagging to get labels
# store in cloud
