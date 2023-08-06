""" Fractal AI research
"""
import os
import shutil
from typing import List

import click
import cv2
import pandas as pd
import torch
import torch.hub
from sklearn.metrics import fbeta_score
from tqdm import tqdm

from fractalai.datasets.agu import get_transforms
from fractalai.datasets.dataloader import build_data_loader
from fractalai.datasets.dataset import CSVDataloader  # sk

from .utils import get_config, get_model


def call_dataset(config: dict):
    if config["dataset_type"] == "csv":
        return CSVDataloader.infer
        # return FractalDL.infer    #sk
    else:
        raise ValueError("The following dataloader is not written")


def call_output_activation_func(config: dict):
    if config["activation"] == "softmax2d":
        return torch.nn.Softmax(dim=1)
    else:
        raise ValueError("This activation function is not available. please raise an issue or PR if required")


def load_essentials(config: dict, weights: str):
    _, transforms = get_transforms(config)
    read_img = call_dataset(config)
    model = get_model(config)
    if "https://" in weights:
        state_dict = torch.hub.load_state_dict_from_url(weights, map_location=lambda storage, location: storage)
    else:
        state_dict = torch.load(weights, map_location=lambda storage, location: storage)
    model.load_state_dict(state_dict)
    if torch.cuda.is_available():
        model = model.cuda()
    model = model.eval()
    return read_img, transforms, model


def infer_img(config_path: str, img_loc: str, weights: str, verbose: bool = True):
    config = get_config(config_path)
    read_img, transforms, model = load_essentials(config, weights)
    with torch.no_grad():
        img = read_img(img_loc, transforms)
        out = model(img)
    out_act = call_output_activation_func(config)(out)
    labels = config.labels
    argmax = int(out_act.argmax(1))
    maxi = out_act.max()
    label = labels[argmax]
    fout = {"label": label, "prob": float(maxi.cpu())}
    if verbose:
        print(fout)
    return fout


def infer_many(config_path: str, list_of_imgs: List[str], weights: str):

    all_prob_data = []
    config = get_config(config_path)
    labels = config.labels
    read_img, transforms, model = load_essentials(config, weights)
    with torch.no_grad():
        for img_loc in tqdm(list_of_imgs):
            img = read_img(img_loc, transforms)
            out = model(img)
            all_prob = list(torch.softmax(out[0], dim=0).cpu().numpy())
            all_prob.insert(0, img_loc)
            all_prob_data.append(all_prob)

        all_prob_df = pd.DataFrame(all_prob_data)
        labels = [lbl + "_prob" for lbl in labels]
        labels.insert(0, "img_loc")
        all_prob_df.columns = labels
    print(all_prob_df.head())
    return all_prob_df


def infer_video(config_path: str, video_loc: str, weights: str, save_loc: str = "predict.mp4"):
    config = get_config(config_path)
    read_img, transforms, model = load_essentials(config, weights)
    video = cv2.VideoCapture(video_loc)  # "/nfs/72_datasets/truth_initiative/title_01_cut_01.mp4"
    fourcc = cv2.VideoWriter_fourcc("M", "J", "P", "G")
    frame_width = int(video.get(3))
    frame_height = int(video.get(4))
    out = cv2.VideoWriter(save_loc, fourcc, video.get(5), (frame_width, frame_height))
    labels = [i.strip() for i in open(config.labels, "r")]
    counter = 0
    output = []
    while True:
        ret, image = video.read()
        if not ret:
            break
        image2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = transforms(image=image2)["image"]
        with torch.no_grad():
            if torch.cuda.is_available():
                img = img.cuda()
            outx = model(img.unsqueeze(0))
            outx = call_output_activation_func(config)(outx).detach().cpu().numpy()
        argmax = int(outx.argmax(1))
        maxi = outx.max()
        label = labels[argmax]
        text = label + ": " + str(round(maxi * 100, 2)) + "%"
        image = cv2_img_writer(image, text)
        output.append(["frame_{}".format(counter), label, round(maxi * 100, 2)])
        counter += 1
        out.write(image)
        # if cv2.waitKey(10) & 0xFF == ord('q'):
        #         break
    video.release()
    out.release()

    data = pd.DataFrame(output)
    data.columns = ["frame_num", "pred_label", "pred_prob"]
    data.to_csv(save_loc.rsplit(".")[0] + ".csv", index=False)
    return out, data


def cv2_img_writer(image, text):
    """
    """
    textOrg = (0, 50)
    cv2.rectangle(image, (textOrg[0], textOrg[1] + 100), (textOrg[0] + 300, textOrg[1] - 20), (0, 0, 0), -1)
    cv2.putText(image, text, textOrg, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.2, (0, 0, 255), 2)
    return image


def create_dirs(v1):
    if not os.path.exists(v1):
        os.makedirs(v1)


@click.command()
@click.option("-c", "--config_path", required=True, help="Path to config file")
@click.option("-i", "--video_loc", required=True, help="Path to img loc")
@click.option("-m", "--weights", required=True, help="model weights path")
@click.option("-s", "--save_loc", default="predict.mp4", help="loacation to save the output weight file")
def infer_video_click(config_path: str, video_loc: str, weights: str, save_loc: str = "predict.mp4"):
    out = infer_video(config_path, video_loc, weights, save_loc)
    return out


@click.command()
@click.option("-c", "--config_path", required=True, help="Path to config file")
@click.option("-i", "--img_loc", required=True, help="Path to img loc")
@click.option("-m", "--weights", required=True, help="model weights path")
def infer_img_click(config_path: str, img_loc: str, weights: str, verbose: bool = True):
    fout = infer_img(config_path, img_loc, weights, verbose)
    return fout


@click.command()
@click.option("-c", "--config_path", required=True, help="Path to config file")
@click.option("-p", "--folder_path", required=True, help="Path to folder")
@click.option("-m", "--weights", required=True, help="model weights path")
@click.option("-o", "--output_csv_name", default="cls_output.csv", help="Name of the output csv")
@click.option("-prob_csv", "--all_prob_save", default=False, help="save all class prob values")
def infer_folder(
    config_path: str, folder_path: str, weights: str, output_csv_name: str, all_prob_save: str,
):

    folder = os.path.dirname(output_csv_name)
    if folder != "":
        create_dirs(folder)

    print("Output csv will be save at : ", output_csv_name)

    imgs = os.listdir(folder_path)
    list_of_imgs = [os.path.join(folder_path, i) for i in imgs if ".jpg" in i or ".png" in i]
    df = infer_many(config_path, list_of_imgs, weights)

    config = get_config(config_path)
    labels = config.labels
    lbls = df.apply(lambda row: row[1:].values.argmax(), axis=1)
    lbls = [labels[l] for l in lbls]
    probs = df.apply(lambda row: max(row[1:]), axis=1)

    final_df = pd.DataFrame()
    final_df["img_loc"] = df.img_loc
    final_df["label"] = lbls
    final_df["prob"] = probs

    final_df.to_csv(output_csv_name, index=False)
    print("Output was saved in csv named : ", output_csv_name)

    if all_prob_save:
        prob_output_csv_name = output_csv_name.replace(".csv", "_probs.csv")
        df.to_csv(prob_output_csv_name, index=False)
        print(
            ">>>>>>>>>> All Prob Output CSV was saved in csv named : ", prob_output_csv_name,
        )


@click.command()
@click.option("-csv", "--csv_file", required=True, help="CSV file having cls output ")
@click.option("-save", "--save_folder_path", required=True, help="Folder path to save cls class folders ")
def make_folders_from_csv(csv_file: str, save_folder_path: str):

    df = pd.read_csv(csv_file)
    for cls in list(df.label.unique()):
        folder = os.path.join(save_folder_path, cls)
        create_dirs(folder)

    print("Empty Folders got created")
    for img, lbl, prob in tqdm(zip(df.img_loc, df.label, df.prob)):
        dest_path = os.path.join(save_folder_path, lbl) + "/" + img.rsplit("/")[-1]
        shutil.copy(img, dest_path)

    print("Classes folders created at : ", save_folder_path)


@click.command()
@click.option("-c", "--config_path", required=True, help="Path to config file")
@click.option("-w", "--weight_file_path", required=True, help="Path to weight file")
@click.option("-method", "--method", help="None, micro, macro, weighted")
def infer_val_f1score(config_path: str, weight_file_path: str, method: str = None):
    config = get_config(config_path)
    train_dl, val_dl = build_data_loader(config)
    model = get_model(config)
    if "https://" in weight_file_path:
        state_dict = torch.hub.load_state_dict_from_url(
            weight_file_path, map_location=lambda storage, location: storage
        )
    else:
        state_dict = torch.load(weight_file_path, map_location=lambda storage, location: storage)
        print("Loading given weight file....")

    model.load_state_dict(state_dict)
    if torch.cuda.is_available():
        model = model.cuda()

    model = model.eval()
    y_t = []
    y_p = []
    for x, y in tqdm(val_dl):
        x = x.to("cuda")
        pred = model(x).cpu().detach().numpy()

        for ind in pred:
            y_p.append(int(ind.argmax()))

        for k in y.squeeze(1).numpy():
            y_t.append(int(k))

    print(f"F1 Score(method:{method}): {fbeta_score(y_t, y_p, average=method, beta=1)}")
