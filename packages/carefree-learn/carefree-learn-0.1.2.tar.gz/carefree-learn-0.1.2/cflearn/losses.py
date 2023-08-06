import torch

import torch.nn as nn

from typing import *
from torch.nn import functional
from abc import ABCMeta, abstractmethod


class LossBase(nn.Module, metaclass=ABCMeta):
    @abstractmethod
    def forward(self,
                predictions: torch.Tensor,
                target: torch.Tensor) -> torch.Tensor:
        pass


class FocalLoss(LossBase):
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self._eps = config.setdefault("eps", 1e-6)
        self._gamma = config.setdefault("gamma", 2.)
        alpha = config.setdefault("alpha", None)
        if isinstance(alpha, (int, float)):
            alpha = [alpha, 1 - alpha]
        elif isinstance(alpha, (list, tuple)):
            alpha = list(alpha)
        self._alpha = alpha

    def forward(self,
                predictions: torch.Tensor,
                target: torch.Tensor) -> torch.Tensor:
        logits_mat, target_column = predictions.view(-1, predictions.shape[-1]), target.view(-1, 1)
        prob_mat = functional.softmax(logits_mat, dim=1) + self._eps
        gathered_prob_flat = prob_mat.gather(dim=1, index=target_column).view(-1)
        gathered_log_prob_flat = gathered_prob_flat.log()
        if self._alpha is not None:
            if isinstance(self._alpha, list):
                self._alpha = torch.tensor(self._alpha).to(predictions)
            alpha_target = self._alpha.gather(dim=0, index=target_column.view(-1))
            gathered_log_prob_flat = gathered_log_prob_flat * alpha_target
        return (-gathered_log_prob_flat * (1 - gathered_prob_flat) ** self._gamma).mean()


__all__ = ["FocalLoss"]
