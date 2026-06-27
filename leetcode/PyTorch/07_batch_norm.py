import torch
from torch_judge import check


def my_batch_norm(
    x: torch.Tensor,
    gamma: torch.Tensor,
    beta: torch.Tensor,
    running_mean: torch.Tensor,
    running_var: torch.Tensor,
    eps: float = 1e-5,
    momentum: float = 0.1,
    training: bool = True,
) -> torch.Tensor:

    if not training:
        mu = running_mean
        var = running_var
    else:
        mu = x.mean(dim=0, keepdim=True)
        std = x.std(dim=0, keepdim=True, unbiased=False)
        var = std**2

        # In place update of running stats
        running_mean[:] = (1 - momentum) * running_mean + momentum * mu
        running_var[:] = (1 - momentum) * running_var + momentum * var

    return gamma * (x - mu) / torch.sqrt(var + eps) + beta


if __name__ == "__main__":
    check("batchnorm")

    x = torch.randn(8, 4)
    gamma = torch.ones(4)
    beta = torch.zeros(4)

    # Running stats typically live on the same device and shape as features
    running_mean = torch.zeros(4)
    running_var = torch.ones(4)

    # Training mode: uses batch stats and updates running_mean / running_var
    out_train = my_batch_norm(x, gamma, beta, running_mean, running_var, training=True)
    print("[Train] Output shape:", out_train.shape)
    print("[Train] Column means:", out_train.mean(dim=0))  # should be ~0
    print("[Train] Column stds: ", out_train.std(dim=0))  # should be ~1
    print("Updated running_mean:", running_mean)
    print("Updated running_var:", running_var)

    # Inference mode: uses running_mean / running_var only
    out_eval = my_batch_norm(x, gamma, beta, running_mean, running_var, training=False)
    print("[Eval] Output shape:", out_eval.shape)

    check("batchnorm")
