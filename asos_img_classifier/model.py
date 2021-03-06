####7 model.py

import torch
import matplotlib.pyplot as plt
import torchvision.transforms as transforms

class Model():

    def __init__(self, net, crit, opt, device):
        self.net = net
        self.opt = opt
        self.crit = crit
        self.device = device
        self.transformer = transforms.ToPILImage()

    def train(self, train_images, train_labels, epoch):
        lossplot = []
        for epoch in range(epoch):  # loop over the dataset multiple times

            running_loss = 0.0
            
            for i in range(len(train_labels)):
                # get the inputs; data is a list of [inputs, labels]
                inputs = train_images[i].to(self.device)
                labels = train_labels[i].to(self.device)
                                       
                self.opt.zero_grad()

                # forward + backward + optimize
                outputs = self.net(inputs)
                loss = self.crit(outputs, labels)
                loss.backward()
                self.opt.step()

                # print statistics
                lossplot.append(loss.item())
                running_loss += loss.item()

            print('[%d, %5d] loss: %.3f' %
                (epoch + 1, i + 1, running_loss / len(train_labels)))
            running_loss = 0.0

        plt.plot(lossplot)
        plt.show()
        print('Finished Training')

    def test(self, test_images, test_labels):
        totalright = 0
        for i in range(len(test_labels)):
            # get the inputs; data is a list of [inputs, labels]
            inputs = test_images[i].to(self.device)
            labels = test_labels[i].to(self.device)
            # forward + backward + optimize
            outputs = self.net(inputs)
            net_labels = outputs.argmax()

            error = labels[0] - net_labels
            if not error:
                totalright += 1
         
        img = self.transformer(inputs.squeeze())
        plt.imshow(img)
        plt.show()
        print("true/net label: ",labels,net_labels, "error: ", error)

        acc = totalright/len(test_labels)
