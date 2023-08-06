"""visualization scripts
"""
import math
import os
from typing import List

import click
import cv2
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

from fractalai.engine.utils import get_config


def plot_img_and_labels(img_loc: List[str], pred_prob: List[float], imgs_per_row: int = 3):
    """
    """
    pil_images = [Image.open(i) for i in img_loc]
    batches = math.ceil(len(pil_images) / float(imgs_per_row))
    for i in range(batches):
        imgs = pil_images[i * imgs_per_row : (i + 1) * imgs_per_row]
        lab = pred_prob[i * imgs_per_row : (i + 1) * imgs_per_row]
        fig, ax = plt.subplots(
            nrows=1, ncols=len(imgs), sharex="col", sharey="row", figsize=(5 * (len(imgs)), 4), squeeze=False
        )
        for i, img in enumerate(imgs):
            ax[0, i].imshow(img)
            ax[0, i].set_title(str(lab[i]))


def get_height_width_statistics(img_paths: List[str], label=str, save: bool = False):
    heights = []
    widths = []
    for imgPath in img_paths:
        image = cv2.imread(imgPath)
        w, h = image.shape[1], image.shape[0]
        heights.append(h)
        widths.append(w)

    print("Average image height in ", label, " : ", sum(heights) / len(heights))
    print("Average image width in ", label, " : ", sum(widths) / len(widths))
    if save:
        plt.plot(widths, label=label + "_Width")
        plt.plot(heights, label=label + "_Height")
        plt.xlabel("images")
        plt.ylabel("size")
        plt.legend()
        plt.savefig(label + ".jpg")


@click.command()
@click.option("-c", "--config_path", required=True, help="Path to config file")
@click.option("-label", "--label", required=True, help="train or test")
@click.option("-save", "--save", default=False)
def get_data_statistic(config_path: str, label: str, save: bool):

    config = get_config(config_path)
    root = config.root
    df = pd.read_csv(config.train_loc)
    df_val = pd.read_csv(config.val_loc)
    if "train" in label:
        train_img_paths = [os.path.join(root, img) for img in df.images]
        get_height_width_statistics(train_img_paths, label, save)

    elif "test" in label:
        val_img_paths = [os.path.join(root, img) for img in df_val.images]
        get_height_width_statistics(val_img_paths, label, save)
    else:
        print("Wrong label was given !!!!!!")
