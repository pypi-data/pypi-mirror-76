import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data as data

import torchvision.transforms as transforms
import torchvision.datasets as datasets

from sklearn import metrics
from sklearn import decomposition
from sklearn import manifold
import matplotlib.pyplot as plt
import numpy as np

import copy
import random
import time

from lxtoolkit.cv.cv_models.MLP import MLP
from lxtoolkit.cv.cv_train.img_cla_train import train_model

#---CONSOLE------------------------------------------------------------------------

DATA_ROOT = './data'
PKL_PATH = './PKL/mlp.pkl'
CHANNELS = 1
NUM_CLASSES = 10    #12 classes of output
LEARNING_RATE = 1e-2  
BATCH_SIZE = 32     #this should fit the GPUs; too big batch_size can't be put into the memory
NUM_EPOCHS = 30
VALID_RATIO = 0.8
#-----------------------------------------------------------------------------------


train_data = datasets.MNIST(root = DATA_ROOT, train = True, download = True)

mean = train_data.data.float().mean() / 255
std = train_data.data.float().std() / 255

train_transforms = transforms.Compose([
                            transforms.RandomRotation(5, fill=(0,)),
                            transforms.RandomCrop(28, padding = 2),
                            transforms.ToTensor(),
                            transforms.Normalize(mean = [mean], std = [std])
                                      ])

test_transforms = transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize(mean = [mean], std = [std])
                                     ])
                                
train_data = datasets.MNIST(root = DATA_ROOT, 
                            train = True, 
                            download = True, 
                            transform = train_transforms)

test_data = datasets.MNIST(root = DATA_ROOT, 
                           train = False, 
                           download = True, 
                           transform = test_transforms)

VALID_RATIO = 0.9

n_train_examples = int(len(train_data) * VALID_RATIO)
n_valid_examples = len(train_data) - n_train_examples

train_data, valid_data = data.random_split(train_data, 
                                           [n_train_examples, n_valid_examples])

valid_data = copy.deepcopy(valid_data)
valid_data.dataset.transform = test_transforms


train_iterator = data.DataLoader(train_data, 
                                 shuffle = True, 
                                 batch_size = BATCH_SIZE)

valid_iterator = data.DataLoader(valid_data, 
                                 batch_size = BATCH_SIZE)

test_iterator = data.DataLoader(test_data, 
                                batch_size = BATCH_SIZE)


model = MLP(784, 10)
optimizer = optim.Adam(model.parameters())
criterion = nn.CrossEntropyLoss()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
criterion = criterion.to(device)

train_model(model, train_iterator, valid_iterator, optimizer, device, PKL_PATH, NUM_EPOCHS)
