import click
import torch
from segmentation_models_pytorch.utils import base
from segmentation_models_pytorch.utils.base import Activation
from segmentation_models_pytorch.utils.metrics import Accuracy, Fscore, IoU

from fractalai.engine.utils import get_config


def metric(cfg):
    return {
        "accuracy": get_accuracy(cfg),
        "f1_score": Fscore(eps=1.0, beta=1, activation=cfg.activation),
        "iou": IoU(activation=cfg.activation, threshold=cfg.threshold),
    }


def get_accuracy(cfg):
    acc = {
        "segmentation": Accuracy(activation=cfg.activation, threshold=cfg.threshold),
        "classification": ClsAccuracy(activation=cfg.activation, threshold=cfg.threshold),
    }

    return acc[cfg.mtype]


def get_metric(cfg):
    assert "metrics" in cfg.keys(), "Metrics is not defined in config file"
    req_metrics = metric(cfg)
    metrics = [req_metrics[i] for i in cfg.metrics]
    return metrics


@click.command()
@click.option("-c", "--config_path", required=True, help="Path to config file")
def check_metrics(config_path: str):
    config = get_config(config_path)
    print(get_metric(config), [i.__name__ for i in get_metric(config)])


class ClsAccuracy(base.Metric):
    def __init__(self, threshold=0.5, activation=None, ignore_channels=None, **kwargs):
        super().__init__(**kwargs)
        self.threshold = threshold
        self.activation = Activation(activation)
        self.ignore_channels = ignore_channels

    def forward(self, y_pr, y_gt):
        y_pr = self.activation(y_pr)
        return accuracy(y_pr, y_gt)


def accuracy(pr, gt):
    pr = torch.argmax(pr, 1)
    gt = gt.squeeze(1)
    tp = torch.sum(gt == pr).float()
    score = tp / gt.shape[0]
    return score
