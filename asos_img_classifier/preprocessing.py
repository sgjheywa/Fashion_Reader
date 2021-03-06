####6 preprocessing.py
import torch
import torchvision.transforms as transforms
import pandas as pd
from PIL import Image
# convert to torch training set

def build_torch_dataset(df, bs, clothing_labels):
    images = []
    labels = []
    toimg = transforms.ToPILImage()
    totens = transforms.ToTensor()
    resizer = transforms.Resize(256)
    cropper = transforms.CenterCrop(244)
    norm = transforms.Normalize((0.5,0.5,0.5), (0.5,0.5,0.5))

    transform_img = transforms.Compose([resizer, cropper, totens, norm])
    for idx, row in df.iterrows():
        l = [clothing_labels.index(row['label'])]
        labels.append(torch.tensor(l))
        imgt = transform_img(Image.open(row['fname'])).unsqueeze(0)
        images.append(imgt)
    return images, labels

def batch_up(imgs, l, batch):
    batch_imgs = []
    batch_l = []
    numbatches = len(imgs)//batch

    for i in range(numbatches):
        b_imgs = torch.cat(imgs[i*batch : i*batch + batch])
        b_l = torch.cat(l[i*batch : i*batch + batch])
        batch_imgs.append(b_imgs)
        batch_l.append(b_l)
    return  batch_imgs, batch_l
