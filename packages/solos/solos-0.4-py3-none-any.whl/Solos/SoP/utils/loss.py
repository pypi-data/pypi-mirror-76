import torch
from torch import nn
from torch.nn.functional import binary_cross_entropy_with_logits, cross_entropy

__all__ = ['BCEWithLogitsLoss']


class BCEWithLogitsLoss(torch.nn.Module):
    def __init__(self, weighted_loss):
        super().__init__()
        self.weighted_loss = weighted_loss

    def forward(self, pred, gt, vs, *args):
        if self.weighted_loss:
            loss = binary_cross_entropy_with_logits(pred, gt, vs[-1].to(pred.device))
        else:
            loss = binary_cross_entropy_with_logits(pred, gt)
        return loss
