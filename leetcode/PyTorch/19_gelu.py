import math
import os

import plotly.express as px
import torch
from torch_judge import check

torch.set_default_device(os.environ.get("TORCH_DEVICE", "cpu"))


def my_gelu(x):
    # Gaussian Error Linear Unit (GELU) activation function
    return x * 0.5 * (1 + torch.erf(x / math.sqrt(2)))


def plot_gelu():
    x = torch.linspace(-5, 5, 100)
    y = my_gelu(x)
    fig = px.line(x=x.cpu().numpy(), y=y.cpu().numpy(), title="GELU Activation Function")
    fig.show()


if __name__ == "__main__":
    # 🧪 Debug
    x = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0])
    print("Output:", my_gelu(x))
    print("Ref:   ", torch.nn.functional.gelu(x))

    check("gelu")

    plot_gelu()
