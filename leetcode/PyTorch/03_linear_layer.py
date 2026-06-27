import math

import torch
import torch.nn as nn
from torch_judge import check


class SimpleLinear:
    """Fully connected linear layer: y = xW^T + b."""

    def __init__(self, in_features: int, out_features: int):
        self._in_features = in_features
        self._out_features = out_features

        scale = 1 / math.sqrt(self._in_features)
        self.weight = nn.Parameter(
            scale * torch.rand(out_features, in_features), requires_grad=True
        )
        self.bias = nn.Parameter(torch.zeros(out_features), requires_grad=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x @ self.weight.T + self.bias


if __name__ == "__main__":
    layer = SimpleLinear(8, 4)
    print("W shape:", layer.weight.shape)  # should be (4, 8)
    print("b shape:", layer.bias.shape)  # should be (4,)

    x = torch.randn(2, 8)
    y = layer.forward(x)
    print("Output shape:", y.shape)  # should be (2, 4)

    check("linear")
