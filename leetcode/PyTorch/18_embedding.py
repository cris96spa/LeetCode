import os

import torch
import torch.nn as nn
from torch_judge import check

torch.set_default_device(os.environ.get("TORCH_DEVICE", "cpu"))


class MyEmbedding(nn.Module):
    def __init__(self, num_embeddings: int, embedding_dim: int):
        # num_embeddings determines the size of the vocabulary
        # embedding_dim the size of each embedding vector, also referred to as d_model
        super().__init__()
        self.weight = nn.Parameter(torch.randn(num_embeddings, embedding_dim))

    def forward(self, indices: torch.Tensor) -> torch.Tensor:
        return self.weight[indices]


if __name__ == "__main__":
    emb = MyEmbedding(10, 4)
    idx = torch.tensor([0, 3, 7])
    print("Output shape:", emb(idx).shape)
    print("Matches manual:", torch.equal(emb(idx)[0], emb.weight[0]))

    check("embedding")
