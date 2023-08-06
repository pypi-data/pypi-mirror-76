import click
import torch.nn as nn
from segmentation_models_pytorch.utils.losses import BCEWithLogitsLoss, CrossEntropyLoss, DiceLoss

from fractalai.engine.utils import get_config
from fractalai.utils.metrics import get_metric


def losses(cfg):
    return {
        "cce_loss": get_cce_loss(cfg),
        "dice_loss": DiceLoss(eps=1.0, beta=1, activation=cfg.activation),
        "bce_loss": BCEWithLogitsLoss(),
    }


def get_cce_loss(cfg):
    if cfg.mtype == "classification":
        return CCELoss()
    elif cfg.mtype == "segmentation":
        return CrossEntropyLoss()
    else:
        raise NotImplementedError(f"This repo doesnt support {cfg.mtype}")


def get_losses(cfg):
    assert "loss_name" in cfg.keys(), "Losses is not defined in config file"
    return losses(cfg)[cfg.loss_name]


@click.command()
@click.option("-c", "--config_path", required=True, help="Path to config file")
def check_metrics(config_path: str):
    config = get_config(config_path)
    print(get_metric(config))


class CCELoss(nn.Module):
    __name__ = "cce_loss"

    def __init__(self):
        super().__init__()
        self.loss = nn.CrossEntropyLoss(reduction="mean")

    def forward(self, y_pr, y_gt):
        y_gt = y_gt.view(-1)
        return self.loss(y_pr, y_gt)


class BCELoss(nn.Module):
    __name__ = "bce_loss"

    def __init__(self):
        super().__init__()
        self.loss = nn.BCEWithLogitsLoss(reduction="mean")

    def forward(self, y_pr, y_gt):
        return self.loss(y_pr, y_gt)
