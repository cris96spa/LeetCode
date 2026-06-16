import os

import torch
import torch.nn as nn
from torch_judge import check

torch.set_default_device(os.environ.get("TORCH_DEVICE", "cpu"))


class MyDropout(nn.Module):
    def __init__(self, p=0.5):
        super().__init__()
        self.p = p

    def forward(self, x):
        if self.training:
            # Dropout: randomly zero out some elements of the input tensor with probability p
            # scale the remaining elements by 1/(1-p) to maintain the expected value of the input
            return x * (torch.rand_like(x) > self.p) / (1 - self.p)
        else:
            return x


if __name__ == "__main__":
    d = MyDropout(p=0.5)
    d.train()
    x = torch.ones(10)
    print("Train:", d(x))
    d.eval()
    print("Eval: ", d(x))

    check("dropout")
