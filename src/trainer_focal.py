"""
CosmoAi - FocalLossV2 with Shangraw Gap coherence
by Jesse Shangraw, Kingston Ontario
v1.1 - adds 45Hz-like synchronous bursts
"""
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

class FocalLossV2(nn.Module):
    def __init__(self, alpha=0.25, gamma=2.0, reduction='mean'):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, inputs, targets):
        ce_loss = F.cross_entropy(inputs, targets, reduction='none')
        pt = torch.exp(-ce_loss)
        focal = self.alpha * (1 - pt) ** self.gamma * ce_loss
        
        if self.reduction == 'mean':
            return focal.mean()
        elif self.reduction == 'sum':
            return focal.sum()
        return focal

def quick_demo(n_samples=2000, n_features=12, coherence_ratio=0.05):
    """
    Generates imbalanced data with Shangraw Gap bursts.
    - 95% background noise (void)
    - 5% coherent bursts (45Hz-like phase lock)
    Returns X, y ready for PyTorch
    """
    # base noise = cosmic void
    X = np.random.normal(0, 1, (n_samples, n_features)).astype(np.float32)
    y = np.zeros(n_samples, dtype=np.int64)
    
    # Step 1: pick rare events
    n_coh = int(n_samples * coherence_ratio)
    idx = np.random.choice(n_samples, n_coh, replace=False)
    
    # Step 2: inject 45Hz-like pattern (Shangraw Gap analog)
    # In brain: 45Hz = neurons fire together
    # In CosmoAi: features align in phase
    t = np.linspace(0, 1, n_features)
    pattern_45hz = np.sin(2 * np.pi * 45 * t)  # 45 cycles
    X[idx] += pattern_45hz * 2.5  # boost coherent samples
    
    # Step 3: add explicit coherence feature
    # This is the "Gap detector" - high when features align
    coherence = np.abs(X).mean(axis=1, keepdims=True).astype(np.float32)
    X = np.hstack([X, coherence])  # now n_features+1
    
    y[idx] = 1  # label coherent bursts as rare class
    
    return X, y

def train_step(model, X, y, loss_fn, optimizer):
    model.train()
    optimizer.zero_grad()
    outputs = model(torch.tensor(X))
    loss = loss_fn(outputs, torch.tensor(y))
    loss.backward()
    optimizer.step()
    return float(loss)
