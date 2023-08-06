import torch
from .cal_acc import cal_acc

def eval(model, iterator, criterion, device, k = 0):
    epoch_len = len(iterator)
    epoch_loss = 0.0
    epoch_acc_1 = 0.0
    epoch_acc_k = 0.0

    # turn off the auto gradient descent and back prop
    model.eval()
    with torch.no_grad():

        for (x, y) in iterator:
            x = x.to(device)
            y = y.to(device)

            # there could be y_pred, _ = model(x1, x2) etc.
            y_pred = model(x)
            loss = criterion(y_pred, y)
            acc_1 = cal_acc(y_pred, y)
            acc_k = cal_acc(y_pred, y, k)

            epoch_loss += loss.item()
            epoch_acc_1 += acc_1.item()
            epoch_acc_k += acc_k.item()
        
    epoch_loss /= epoch_len
    epoch_acc_1 /= epoch_len
    epoch_acc_k /= epoch_len
    if epoch_acc_k >= 0:
        return epoch_loss, epoch_acc_1, epoch_acc_k
    else:
        return epoch_loss, epoch_acc_1