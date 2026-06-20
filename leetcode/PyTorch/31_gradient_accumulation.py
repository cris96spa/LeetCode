import os

import torch
import torch.nn as nn
from torch_judge import check

torch.set_default_device(os.environ.get("TORCH_DEVICE", "cpu"))


def accumulated_step(
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    loss_fn: nn.Module,
    micro_batches: list[tuple[torch.Tensor, torch.Tensor]],
) -> float:
    # Zero out gradients
    optimizer.zero_grad()
    num_batches = len(micro_batches)

    if num_batches == 0:
        raise ValueError("No micro-batches provided for gradient accumulation.")
    total_loss = 0.0
    for x, y in micro_batches:
        loss = loss_fn(model(x), y) / num_batches
        total_loss += loss.item()
        loss.backward()
    optimizer.step()

    return total_loss


if __name__ == "__main__":
    model = nn.Linear(4, 2)
    opt = torch.optim.SGD(model.parameters(), lr=0.01)
    loss = accumulated_step(
        model, opt, nn.MSELoss(), [(torch.randn(2, 4), torch.randn(2, 2)) for _ in range(4)]
    )
    print("Loss:", loss)

    check("gradient_accumulation")
