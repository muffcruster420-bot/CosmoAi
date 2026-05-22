"""
CosmoAi Demo - FocalLossV2 with Shangraw Gap
by Jesse Shangraw
"""
import streamlit as st
import numpy as np
import torch
import torch.nn as nn
from src.trainer_focal import FocalLossV2, quick_demo

st.set_page_config(page_title="CosmoAi - Shangraw Gap", layout="centered")
st.title("CosmoAi: Shangraw Gap Detector")
st.write("by Jesse Shangraw • Kingston, Ontario")

st.markdown("**Test FocalLossV2 on 45Hz-like coherent bursts**")

# Step 2 controls
gamma = st.slider("Focal Gamma (focus on hard examples)", 0.5, 5.0, 2.0, 0.1)
alpha = st.slider("Alpha (rare class weight)", 0.1, 0.9, 0.25, 0.05)
gap_strength = st.slider("Shangraw Gap Strength (coherence %)", 1, 20, 5, 1)

if st.button("Run Demo"):
    # generate data with coherence
    X, y = quick_demo(n_samples=2000, n_features=12, coherence_ratio=gap_strength/100)
    
    # simple model
    model = nn.Sequential(
        nn.Linear(X.shape[1], 32),
        nn.ReLU(),
        nn.Linear(32, 2)
    )
    
    loss_fn = FocalLossV2(alpha=alpha, gamma=gamma)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    
    losses = []
    for epoch in range(30):
        model.train()
        optimizer.zero_grad()
        out = model(torch.tensor(X))
        loss = loss_fn(out, torch.tensor(y))
        loss.backward()
        optimizer.step()
        losses.append(float(loss))
    
    # results
    model.eval()
    with torch.no_grad():
        preds = model(torch.tensor(X)).argmax(1).numpy()
    
    rare_detected = (preds[y==1] == 1).sum()
    rare_total = (y==1).sum()
    
    st.success(f"Detected {rare_detected}/{rare_total} coherent bursts ({100*rare_detected/max(1,rare_total):.1f}%)")
    st.line_chart(losses)
    
    st.caption(f"Data shape: {X.shape} (last column = coherence feature). Gap strength: {gap_strength}%")
    st.caption("Higher gamma = ignores background void, focuses on rare 45Hz-like events")
