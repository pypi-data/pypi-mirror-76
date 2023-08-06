# Fractal AI

import inspect
import os
from typing import Sequence

import click
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset as BaseDataset

from fractalai.datasets.agu import get_transforms, shuffle, to_tensor
from fractalai.engine.utils import get_config


class CSVDataloader(BaseDataset):
    """ segmentation and classification dataloader
    """

    def __init__(self, df, dtransforms=None, root: str = "", mtype: str = "classification", labels: Sequence[str] = []):
        self.df = df
        self.root = root
        self.images_fps = self.df["images"].values.tolist()
        self.labels_fps = self.df["labels"].values.tolist()  #
        self.mtype = mtype

        self.class_values = len(labels)
        self.labels_mapping = {k: v for k, v in enumerate(labels)}
        self.reverse_mapping = {v: k for k, v in enumerate(labels)}
        self.dtransforms = dtransforms

    def __getitem__(self, i):

        # read data

        image = cv2.imread(os.path.join(self.root, self.images_fps[i]))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if self.mtype == "classification":
            label = np.asarray([self.reverse_mapping[self.labels_fps[i]]])
        else:
            label = cv2.imread(os.path.join(self.root, self.labels_fps[i]), 0)
            label = np.uint8(label)
            label = np.expand_dims(label, 2)

        if self.dtransforms:
            if self.mtype == "classification":
                sample = self.dtransforms(image=image)
                image = sample["image"]
            else:
                sample = self.dtransforms(image=image, mask=label)
                image, label = sample["image"], sample["mask"]
                label[label > 0] = 1

        return image, label

    def __len__(self):
        return len(self.images_fps)

    def total_labels(self):
        return self.labels_fps.unique().shape

    @classmethod
    def infer(cls, img_loc, transforms=None):
        img = cv2.imread(img_loc)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if transforms is not None:
            img = transforms(image=img)
            img = img["image"]
        else:
            img = shuffle(to_tensor(img))
        img = img.unsqueeze(0)

        if torch.cuda.is_available():
            img = img.cuda()
        return img


def get_dataset(config):
    train_csv_file = config["train_loc"]
    train_df = pd.read_csv(train_csv_file)
    valid_csv_file = config["val_loc"]
    valid_df = pd.read_csv(valid_csv_file)
    train_transforms, val_transforms = get_transforms(config)

    train_root = config["train_root"]
    test_root = config["test_root"]

    if config["dataset_type"] == "csv":
        keys_required = inspect.getfullargspec(CSVDataloader)
        keys_essentials = keys_required[0][1:]
        fdict = {k: v for k, v in config.items() if k in keys_essentials}
        train_dataset = CSVDataloader(train_df, train_transforms, train_root, **fdict)
        valid_dataset = CSVDataloader(valid_df, val_transforms, test_root, **fdict)
    else:
        print("Dataset_type not implemented !!!!")
    return train_dataset, valid_dataset


@click.command()
@click.option("-c", "--config_path", required=True, help="Path to config file")
def run_dataset(config_path: str):
    config = get_config(config_path)
    train_dataset, valid_dataset = get_dataset(config)
    index = np.random.randint(len(train_dataset))
    img, mask = train_dataset[index]
    print(img.shape, mask.shape)


def visualize_seg(save_path=None, **images):
    """PLot images in one row.
     Obtained this piece of code from
     https://github.com/qubvel/segmentation_models.pytorch/blob/master/examples/cars%20segmentation%20(camvid).ipynb
    """
    n = images["image"].shape[0]
    fig = plt.figure(figsize=(10, 15))
    for i in range(0, n):
        fig.add_subplot(n, 2, 2 * i + 1)
        plt.imshow(images["image"][i, :, :, :])
        fig.add_subplot(n, 2, 2 * (i + 1))
        plt.imshow(np.squeeze(images["mask"][i, :, :, :]))

    if save_path is None:
        fig.show()
    else:
        import os

        print("Visualization saved at {}".format(os.path.join(os.getcwd(), save_path)))
        fig.savefig(os.path.join(os.getcwd(), save_path))


def visualize_cls(save_path=None, **images):
    """PLot images in one row.
     Obtained this piece of code from
     https://github.com/qubvel/segmentation_models.pytorch/blob/master/examples/cars%20segmentation%20(camvid).ipynb
    """
    n = images["image"].shape[0]
    fig = plt.figure(figsize=(10, 15))
    for i in range(0, n):
        fig.add_subplot(n, 1, i + 1)
        plt.imshow(images["image"][i, :, :, :])
        plt.title("label - " + images["labels"][images["label_stack"][i][0]])

    if save_path is None:
        fig.show()
    else:
        import os

        print("Visualization saved at {}".format(os.path.join(os.getcwd(), save_path)))
        fig.savefig(os.path.join(os.getcwd(), save_path))


@click.command()
@click.option("-c", "--config_path", required=True, help="Path to config file")
@click.option("-n", "--number_of_images", required=True, help="number of images")
@click.option("-s", "--save_path", default="visualize.jpg", help="path to save the visualization")
def visualize_random_example(config_path: str, number_of_images: int, save_path: str):
    config = get_config(config_path)
    config.post_transform_type = False
    train_dataset, valid_dataset = get_dataset(config)
    list_indx = np.random.randint(len(train_dataset), size=int(number_of_images))
    img_stack, mask_stack = train_dataset[list_indx[0]]
    img_stack = np.expand_dims(img_stack, axis=0)
    mask_stack = np.expand_dims(mask_stack, axis=0)
    for i in range(1, len(list_indx)):
        img, mask = train_dataset[list_indx[i]]
        img = np.expand_dims(img, axis=0)
        mask = np.expand_dims(mask, axis=0)
        img_stack = np.vstack((img_stack, img))
        mask_stack = np.vstack((mask_stack, mask))
    if config.mtype == "classification":
        visualize_cls(save_path, image=img_stack, label_stack=mask_stack, labels=config.labels)
    else:
        visualize_seg(save_path, image=img_stack, mask=mask_stack)
