import torch
from torch_judge import check


def my_layer_norm(x: torch.Tensor, gamma: torch.Tensor, beta: torch.Tensor, eps=1e-5):
    mu = torch.mean(x, dim=-1, keepdim=True)
    std = torch.std(x, dim=-1, keepdim=True, unbiased=False)

    return gamma * (x - mu) / torch.sqrt(std**2 + eps) + beta


if __name__ == "__main__":
    x = torch.randn(2, 8)
    gamma = torch.ones(8)
    beta = torch.zeros(8)

    out = my_layer_norm(x, gamma, beta)
    ref = torch.nn.functional.layer_norm(x, [8], gamma, beta)

    print("Your output mean:", out.mean(dim=-1))  # should be ~0
    print("Your output std: ", out.std(dim=-1))  # should be ~1
    print("Match ref?      ", torch.allclose(out, ref, atol=1e-4))

    check("layernorm")
