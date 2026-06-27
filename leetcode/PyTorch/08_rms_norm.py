import torch
from torch_judge import check


def rms_norm(x: torch.Tensor, weight: torch.Tensor, eps: float = 1e-6) -> torch.Tensor:
    """Apply RMSNorm.

    RMSNorm(x) = x / RMS(x) * weight; RMS(x) = sqrt(1/d * sum(x_i**2 + eps))
    """
    d = x.shape[-1]
    rms = torch.sqrt(torch.sum(x**2 + eps, dim=-1, keepdim=True) / d)
    return x * weight / rms


if __name__ == "__main__":
    # 🧪 Debug
    x = torch.randn(2, 8)
    w = torch.ones(8)
    out = rms_norm(x, w)
    print("Output shape:", out.shape)
    print("RMS of output:", out.pow(2).mean(dim=-1).sqrt())  # should be ~1

    check("rmsnorm")
