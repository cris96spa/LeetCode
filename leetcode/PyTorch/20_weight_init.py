import math
import os

import plotly.graph_objects as go
import torch
from torch_judge import check

torch.set_default_device(os.environ.get("TORCH_DEVICE", "cpu"))


def kaiming_init(weight: torch.Tensor) -> None:
    # The Kaiming (He) initialization is designed to keep the variance of
    # the activations and gradients approximately the same across
    # every layer. It is obtained by drawing samples from a normal distribution with mean 0 and
    # standard deviation sqrt(2 / fan_in)
    fan_in = weight.shape[1]  # Number of input units in the weight tensor
    std = math.sqrt(2 / fan_in)
    with torch.no_grad():
        weight.normal_(mean=0.0, std=std)


def plot_weight_distributions(before: torch.Tensor, after: torch.Tensor):
    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=before.cpu().flatten().numpy(),
            nbinsx=50,
            name="Before (randn)",
            opacity=0.6,
        )
    )
    fig.add_trace(
        go.Histogram(
            x=after.cpu().flatten().numpy(),
            nbinsx=50,
            name="After (He init)",
            opacity=0.6,
        )
    )
    fig.update_layout(
        title="Weight Distribution: Before vs After He Initialization",
        xaxis_title="Weight value",
        yaxis_title="Count",
        barmode="overlay",
    )
    fig.show()


if __name__ == "__main__":
    w = torch.randn(256, 512)
    before = w.clone()
    kaiming_init(w)
    print(f"Mean: {w.mean():.4f} (expect ~0)")
    print(f"Std:  {w.std():.4f} (expect {math.sqrt(2 / 512):.4f})")

    plot_weight_distributions(before, w)
    check("weight_init")
