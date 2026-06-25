import math
import os

import torch
import torch.nn as nn
from torch_judge import check

torch.set_default_device(os.environ.get("TORCH_DEVICE", "cpu"))


class LoRALinear(nn.Module):
    """LoRA (Low-Rank Adaptation) for Linear layers.

    h = W x + alpha/r * A B x

    where W is the frozen weight of the original linear layer, A and B are learnable
    low-rank matrices, alpha is a scaling factor, and r is the rank of the low-rank matrices.
    """

    def __init__(self, in_features: int, out_features: int, rank: int, alpha: float = 1.0):
        super().__init__()

        self.in_features = in_features
        self.out_feature = out_features

        if rank > max(in_features, self.out_feature) or rank < 1:
            raise ValueError(
                f"Invalid rank, should be [1, {max(in_features, self.out_feature)}), got {rank}"
            )
        self.rank = rank
        self.alpha = alpha
        self.scaling = self.alpha / self.rank

        # Create a dense layer
        self.linear = nn.Linear(
            in_features=in_features,
            out_features=out_features,
        )
        for param in self.linear.parameters():
            param.requires_grad = False

        self.lora_A = nn.Parameter(torch.empty(rank, in_features))
        self.lora_B = nn.Parameter(torch.empty(out_features, rank))

        self._init_lora_parameters()

    def _init_lora_parameters(self):
        nn.init.kaiming_uniform_(self.lora_A, a=math.sqrt(5))
        nn.init.zeros_(self.lora_B)

    def forward(self, x):
        lin_out = self.linear(x)

        # x [n x in_features]
        # A [rank x in_features]
        # B [out_features x rank]

        lora_out = x @ (self.lora_B @ self.lora_A).T

        return lin_out + self.scaling * lora_out


if __name__ == "__main__":
    layer = LoRALinear(16, 8, rank=4)
    x = torch.randn(2, 16)
    print("Output:", layer(x).shape)
    print("Trainable:", sum(p.numel() for p in layer.parameters() if p.requires_grad))
    print("Total:    ", sum(p.numel() for p in layer.parameters()))
    check("lora")
