""" Fractal AI research

uses albumentations and works together with everything
# Refrences
- https://github.com/albu/albumentations/blob/master/notebooks/example.ipynb
"""

import pprint

import albumentations as albu
import click
import torch
from albumentations import (
    CLAHE,
    Blur,
    Compose,
    Flip,
    GaussNoise,
    HueSaturationValue,
    IAAAdditiveGaussianNoise,
    IAAEmboss,
    IAAPiecewiseAffine,
    IAASharpen,
    MedianBlur,
    MotionBlur,
    Normalize,
    OneOf,
    OpticalDistortion,
    PadIfNeeded,
    RandomBrightnessContrast,
    RandomRotate90,
    Resize,
    ShiftScaleRotate,
    Transpose,
)


def get_transforms(config: dict):
    ttype = config["pre_transform_type"]
    print(f"using {ttype} transforms")
    if ttype == "simple":
        train, val = simple_transforms(config)
    elif ttype == "adv1":
        train, val = advanced_transforms(config)
    else:
        raise NotImplementedError("Following transforms are not implemented")

    if config["post_transform_type"]:
        trainp, valp = get_post_transforms(config)
        train.extend(trainp)
        val.extend(valp)
    return Compose(train), Compose(val)


def simple_transforms(config: dict):
    """border_mode=cv2.BORDER_CONSTANT, value=0
    """
    height = config["height"]
    width = config["width"]
    train_transforms = [
        PadIfNeeded(p=1.0, min_height=height, min_width=width),
        Resize(height, width),
    ]  # , #Flip(p=0.5)]

    val_transforms = [PadIfNeeded(p=1.0, min_height=height, min_width=width), Resize(height, width)]

    return train_transforms, val_transforms


def advanced_transforms(config: dict):
    height, width = config["height"], config["width"]
    train_transforms = [
        RandomRotate90(),
        Flip(),
        Transpose(),
        OneOf([IAAAdditiveGaussianNoise(), GaussNoise()], p=0.2),
        OneOf([MotionBlur(p=0.2), MedianBlur(blur_limit=3, p=0.1), Blur(blur_limit=3, p=0.1)], p=0.2),
        ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.2, rotate_limit=45, p=0.2),
        OneOf([OpticalDistortion(p=0.3), IAAPiecewiseAffine(p=0.3)], p=0.2),
        OneOf([CLAHE(clip_limit=2), IAASharpen(), IAAEmboss(), RandomBrightnessContrast()], p=0.3),
        HueSaturationValue(p=0.3),
        PadIfNeeded(p=1.0, min_height=height, min_width=width),
        Resize(height, width),
    ]

    val_transforms = [PadIfNeeded(p=1.0, min_height=height, min_width=width), Resize(height, width)]
    return train_transforms, val_transforms


def get_post_transforms(config: dict):
    train_transforms = []
    val_transforms = []

    mean = config["mean"]
    std = config["std"]

    if config["post_transform_type"]:
        norm = Normalize(mean=mean, std=std)
        train_transforms.append(norm)
        val_transforms.append(norm)

    f = [
        albu.Lambda(name="transpose", image=shuffle, mask=shuffle),
        albu.Lambda(name="totensor", image=to_tensor, mask=to_tensor),
    ]

    train_transforms = train_transforms + f
    val_transforms = val_transforms + f
    return train_transforms, val_transforms


def shuffle(x, **kwargs):
    return x.transpose(2, 0, 1).astype("float32")


def to_tensor(x, **kwargs):
    return torch.Tensor(x)


def to_mask_tensor(x, **kwargs):
    return torch.Tensor(x).long()


@click.command()
@click.option("-c", "--config_path", required=True, help="Path to config file")
def understand_transforms(config_path: str):
    from fractalai.engine.utils import get_config

    config = get_config(config_path)
    train, val = get_transforms(config)
    pp = pprint.PrettyPrinter(indent=4)
    print("[train transforms]")
    pp.pprint(train)
    print("[val transforms]")
    pp.pprint(val)
