import torch
import torch.nn as nn
import torch.functional as F


class Loss:
    @classmethod
    def dice_loss(self, pred, target, smooth=1.):
        pred = pred.contiguous()
        target = target.contiguous()
        intersection = (pred * target).sum(dim=2).sum(dim=2)
        loss = (1 - ((2. * intersection + smooth) /
                     (pred.sum(dim=2).sum(dim=2) + target.sum(dim=2).sum(dim=2) + smooth)))
        return loss.mean()

    def calc_loss(self, pred, target, metrics, bce_weight=0.5):
        bce = torch.nn.functional.binary_cross_entropy(pred, target)
        pred = torch.sigmoid(pred)
        dice = self.dice_loss(pred, target)
        loss = bce * bce_weight + dice * (1 - bce_weight)
        metrics['bce'] += bce.data.cpu().numpy() * target.size(0)
        metrics['dice'] += dice.data.cpu().numpy() * target.size(0)
        metrics['loss'] += loss.data.cpu().numpy() * target.size(0)
        return loss
