import math
import os

import torch
from torch_judge import check

torch.set_default_device(os.environ.get("TORCH_DEVICE", "cpu"))


def clip_grad_norm(parameters: list[torch.Tensor], max_norm: float) -> float:
    # To clip the gradients, we first compute the total norm of the gradients across all parameters.
    # It it exceeds the specified max_norm, we scale down the gradients by max_norm/total_norm
    # to ensure that the total norm of the gradients is at most max_norm.
    total_norm = math.sqrt(sum(p.grad.norm() ** 2 for p in parameters if p.grad is not None))

    if total_norm > max_norm:
        # Scale the gradients to have a norm of max_norm
        scale = max_norm / (total_norm + 1e-6)
        for p in parameters:
            if p.grad is not None:
                p.grad.mul_(scale)

    return total_norm


if __name__ == "__main__":
    p = torch.randn(100, requires_grad=True)
    # Multiply by a large number to simulate a large gradient
    # then backpropagate to compute the gradient
    (p * 10).sum().backward()
    print("Before:", p.grad.norm().item())

    orig = clip_grad_norm([p], max_norm=1.0)

    print("After: ", p.grad.norm().item())
    print("Original norm:", orig)

    check("gradient_clipping")
