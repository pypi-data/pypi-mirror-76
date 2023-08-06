import torch

# calculate top k accuracy for classification tasks
# by default, top 1 accuracy will be returned
def cal_acc(y_pred, y, k = 1):
    # When calculating accuracy, the auto gradient descent should be turned off

    #more robust
    if k < 1:
        return -1

    with torch.no_grad():
        batch_size = y.shape[0]
        _, topk = y_pred.topk(k, 1)
        topk = topk.t()
        correct_all = topk.eq(y.view(1, -1).expand_as(topk))
        correct_k = correct_all[:k].view(-1).float().sum(0, keepdim = True)
        acc = correct_k / batch_size
    return acc

