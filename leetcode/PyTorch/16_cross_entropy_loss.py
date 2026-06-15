import os

import torch
from torch import Tensor
from torch_judge import check

torch.set_default_device(os.environ.get("TORCH_DEVICE", "cpu"))


def cross_entropy_loss(logits: Tensor, targets: Tensor) -> Tensor:
    # Step 1: Compute log-softmax of logits using the log-sum-exp trick
    max_logits = torch.max(logits, dim=1, keepdim=True).values
    shifted_logits = logits - max_logits
    log_sum_exp = torch.log(torch.sum(torch.exp(shifted_logits), dim=1, keepdim=True))
    log_probs = shifted_logits - log_sum_exp

    # Step 2: Gather the log probabilities corresponding to the target classes
    target_log_probs = log_probs.gather(dim=1, index=targets.unsqueeze(1))

    # Step 3: Compute the mean negative log-likelihood loss
    return -target_log_probs.mean()


if __name__ == "__main__":
    logits = torch.randn(4, 10)
    targets = torch.randint(0, 10, (4,))
    print("Loss:", cross_entropy_loss(logits, targets))
    print("Ref: ", torch.nn.functional.cross_entropy(logits, targets))

    check("cross_entropy")
