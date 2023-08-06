import glob
import json
import random

import click
import pandas as pd

from fractalai.engine.utils import get_config

random.seed(50)


@click.command()
@click.option("-c", "--config_path", required=True, help="Path to config file")
def get_classes(config_path: str):
    config = get_config(config_path)
    assert config.mtype == "classification", "the config_path.mtype is not classification"
    assert config.train_loc.rsplit(".")[-1] == "csv", "the train loc is not a csv file"
    df = pd.read_csv(config.train_loc)
    dft = pd.read_csv(config.val_loc)
    print(f"train: {df['labels'].unique()}")
    print(f"val: {dft['labels'].unique()}")


@click.command()
@click.option("-r1", "--root1", required=True, help="Path to config file")
@click.option("-r2", "--root2", required=True, help="Path to config file")
def make_csv_given_folders(root1: str, root2: str):
    images = glob.glob(root1 + "/*.png")
    random.shuffle(images)
    labels = [root2 + i.rsplit("/")[-1].rsplit(".")[0] + "_mask.png" for i in images]
    cut = int(0.8 * len(images))
    t1, tt1 = images[:cut], labels[:cut]
    t2, tt2 = images[cut:], labels[cut:]
    df = pd.DataFrame([t1, tt1]).T
    dft = pd.DataFrame([t2, tt2]).T
    df.columns = ["images", "labels"]
    dft.columns = ["images", "labels"]
    df.to_csv("datasets/PennFudanPed/train.csv", index=False)
    dft.to_csv("datasets/PennFudanPed/val.csv", index=False)
    print(df.shape, dft.shape)


@click.command()
@click.option("-json", "--json_path", required=True, help="Path to json file")
@click.option("-csv", "--csv_save_path", required=True, help="Path to csv file")
def json_to_csv(json_path: str, csv_save_path: str):

    with open(json_path, "r") as fp:
        jfile = json.load(fp)
    images = []
    labels = []
    for img in jfile["images"]:
        images.append(img["image_id"])
        labels.append(img["image_id"].rsplit("/")[0])

    df = pd.DataFrame()
    df["images"] = images
    df["labels"] = labels
    print(df.head())
    df.to_csv(csv_save_path, index=False)
    print("CSV saved !!")
