import os

import torch
from torch_judge import check

torch.set_default_device(os.environ.get("TORCH_DEVICE", "cpu"))


def my_softmax(x: torch.Tensor, dim: int = -1) -> torch.Tensor:
    # Ensure numerical stability by subtracting the max value from x before exponentiating
    x = x - torch.max(x, dim=dim, keepdim=True).values
    exp_x = torch.exp(x)
    exp_sum = torch.sum(exp_x, dim=dim, keepdim=True)
    return exp_x / exp_sum


if __name__ == "__main__":
    x = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0])
    print("Input: ", x)
    print("Output:", my_softmax(x))
    print("Shape: ", my_softmax(x).shape)

    check("softmax")
