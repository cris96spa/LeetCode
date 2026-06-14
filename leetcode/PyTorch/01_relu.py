import os

import torch
from torch_judge import check

torch.set_default_device(os.environ.get("TORCH_DEVICE", "cpu"))


def relu(x: torch.Tensor) -> torch.Tensor:
    return torch.where(x > 0, x, torch.zeros_like(x))


if __name__ == "__main__":
    x = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0])
    print("Input: ", x)
    print("Output:", relu(x))
    print("Shape: ", relu(x).shape)

    check("relu")
