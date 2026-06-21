import os

import torch
import torch.nn as nn
from torch_judge import check

torch.set_default_device(os.environ.get("TORCH_DEVICE", "cpu"))


class LinearRegression:
    def closed_form(self, X: torch.Tensor, y: torch.Tensor):
        """Normal equation: w = (X^T X)^{-1} X^T y."""
        X = torch.cat((torch.ones(len(X), 1), X), dim=1)
        closed_form = (X.T @ X).inverse() @ X.T @ y
        return closed_form[1:], closed_form[0]

    def gradient_descent(
        self, X: torch.Tensor, y: torch.Tensor, lr: float = 0.01, steps: int = 1000
    ):
        """Manual gradient descent loop."""
        w = torch.zeros(X.shape[1])
        b = torch.zeros(())
        N = X.shape[0]
        for _ in range(steps):
            pred = X @ w + b
            error = pred - y
            grad_w = 2 / N * X.T @ error
            grad_b = 2 / N * error.sum()
            w -= lr * grad_w
            b -= lr * grad_b

        return w, b

    def nn_linear(self, X: torch.Tensor, y: torch.Tensor, lr: float = 0.01, steps: int = 1000):
        """Train nn.Linear with autograd."""
        loss_fn = nn.MSELoss()
        _, d_out = X.shape
        linear_layer = nn.Linear(d_out, 1)
        optim = torch.optim.SGD(
            linear_layer.parameters(),
            lr=lr,
        )
        for _ in range(steps):
            optim.zero_grad()
            loss = loss_fn(linear_layer(X).squeeze(dim=1), y)
            loss.backward()
            optim.step()

        return linear_layer.weight.squeeze(dim=0), linear_layer.bias


if __name__ == "__main__":
    torch.manual_seed(42)
    X = torch.randn(100, 3)
    true_w = torch.tensor([2.0, -1.0, 0.5])
    y = X @ true_w + 3.0

    model = LinearRegression()

    w_cf, b_cf = model.closed_form(X, y)
    print(f"Closed-form:  w={w_cf}, b={b_cf.item():.4f}")

    w_gd, b_gd = model.gradient_descent(X, y, lr=0.05, steps=2000)
    print(f"Grad descent: w={w_gd}, b={b_gd.item():.4f}")

    w_nn, b_nn = model.nn_linear(X, y, lr=0.05, steps=2000)
    print(f"nn.Linear:    w={w_nn}, b={b_nn.item():.4f}")

    print(f"\nTrue:         w={true_w}, b=3.0")

    check("linear_regression")
