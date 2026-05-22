import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import precision_score, recall_score, f1_score

class FocalLossV2(nn.Module):
    '''
    COSMOAI recall booster - substitute for standard focal loss
    Tuned for dark matter halos (rare positives)
    gamma=1.5, alpha=0.75, label_smoothing=0.05
    '''
    def __init__(self, gamma=1.5, alpha=0.75, label_smoothing=0.05):
        super().__init__()
        self.gamma = gamma
        self.alpha = alpha
        self.smooth = label_smoothing
    
    def forward(self, logits, targets):
        targets = targets * (1 - self.smooth) + 0.5 * self.smooth
        bce = F.binary_cross_entropy_with_logits(logits, targets, reduction='none')
        pt = torch.exp(-bce)
        alpha_t = self.alpha * targets + (1 - self.alpha) * (1 - targets)
        loss = alpha_t * (1 - pt) ** self.gamma * bce
        return loss.mean()

def train_epoch(model, loader, opt, device='cpu'):
    model.train()
    total_loss = 0
    all_preds, all_targets = [], []
    
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        opt.zero_grad()
        logits = model(x).squeeze()
        loss = FocalLossV2()(logits, y)
        loss.backward()
        opt.step()
        
        total_loss += loss.item()
        preds = (torch.sigmoid(logits) > 0.45).float()
        all_preds.extend(preds.cpu().numpy())
        all_targets.extend(y.cpu().numpy())
    
    prec = precision_score(all_targets, all_preds, zero_division=0)
    rec = recall_score(all_targets, all_preds, zero_division=0)
    f1 = f1_score(all_targets, all_preds, zero_division=0)
    
    return {'loss': total_loss/len(loader), 'precision': prec, 'recall': rec, 'f1': f1}
