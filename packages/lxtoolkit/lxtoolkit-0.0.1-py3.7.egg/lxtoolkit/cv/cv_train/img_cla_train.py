import os
import torch
import time
from lxtoolkit.cv.cv_evaluation.cal_acc import cal_acc
from lxtoolkit.cv.cv_evaluation.img_cla_eval import eval
from lxtoolkit.cv.cv_evaluation.Miscellaneous import epoch_time
# training default classification networks
# x, y in iterator 
"""
e.g. 
model = LeNet(...)
train_iterator = data.Dataloader(...)
valid_iterator = data.Dataloader(...)
# you can add learning rate decay in the optimizer
optimizer = torch.optim.Adadelta(params, lr=1.0, rho=0.9, eps=1e-06, weight_decay=0)
criterion = nn.CrossEntropyLoss()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# path is where you save your learnt parameters
path = "/Users/blackbeanman/Desktop/project/data/params.pkl" 
epochs = 50
lr = 4e-3

train_model(model, train_iterator, valid_iterator, optimizer, criterion, device, path, epochs, lr)
"""

# the 1st epoch would be unexpectedly slow
# This kind of slowness has nothing to do with the parameter transfer time: All the parameter transfer here are in place
# The cause is the construction of computing graph and some sort of data caching 
def train_model(model, train_iterator, valid_iterator, optimizer, criterion, device, path, epochs):
    #load params
    if os.path.exists(path):
        model.load_state_dict(torch.load(path))
    
    #The best_valid_loss will be used to decide which set of parameters is valuable.
    #And the "valuable"(min valid loss) set are going to be saved as .pkl
    min_valid_loss = float('inf')

    for i in range(epochs):
        start_time = time.time()

        epoch_len = len(train_iterator)
        epoch_loss = 0.0
        epoch_acc = 0.0

        model.train()

        # the (x, y) could be modified to fit other projects: (x, y, l) etc.
        for (x, y) in train_iterator:
            x = x.to(device)
            y = y.to(device)

            optimizer.zero_grad()
            # there could be y_pred, _ = model(x1, x2) etc.
            y_pred = model(x)
            # cal loss and perform back prop
            loss = criterion(y_pred, y)
            loss.backward()
            optimizer.step()

            # there could be acc_1, acc_5 = cal_top5_acc(y_pred, y)
            acc = cal_acc(y_pred, y)

            #!!!!!!!!!!why .item()
            epoch_loss += loss.item()
            epoch_acc += acc.item()

        train_loss = epoch_loss/epoch_len
        train_acc = epoch_acc/epoch_len
        valid_loss, valid_acc = eval(model, valid_iterator, criterion, device)

        # save valuable parameters
        if valid_loss < min_valid_loss:
            min_valid_loss = valid_loss
            torch.save(model.state_dict(), path)
        
        end_time = time.time()
        epoch_mins, epoch_secs = epoch_time(start_time, end_time)

        print('Epoch: {epoch+1:02} | Epoch Time: {epoch_mins}m {epoch_secs}s')
        print('\tTrain Loss: {train_loss:.3f} | Train Acc : {train_acc_1*100:6.2f}')
        print('\tValid Loss: {valid_loss:.3f} | Valid Acc : {valid_acc_1*100:6.2f}')