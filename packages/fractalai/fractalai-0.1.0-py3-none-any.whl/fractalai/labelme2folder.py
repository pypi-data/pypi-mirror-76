import glob
import io
import json
import os

import click
import numpy as np
import PIL.Image
from PIL import Image, ImageDraw
from pycocotools import mask as CocoMask
from tqdm import tqdm


def labels_counter(folder_loc: str):
    """
    count the number of labels
    """
    json_files = glob.glob(folder_loc + "*.json")
    total = len(json_files)
    print("total json files: [{}]".format(total))
    labels_counter: dict = {}
    for num, j in tqdm(enumerate(json_files)):
        jsonf = load_json(j)
        shapes = jsonf["shapes"]
        label = [i["label"] for i in shapes]
        for k in label:
            if k not in labels_counter.keys():
                labels_counter[k] = 1
            else:
                labels_counter[k] += 1
    labels_counter_final = [(k, v) for k, v in labels_counter.items()]
    return labels_counter_final


def load_json(files: str):
    """Load a json file
    """
    with open(files, "r") as fp:
        file = json.load(fp)
    return file


def encode_polygon(points, img_dim):
    """
    points: [[x1, y1], [x2, y2], ....[xn, yn]]
    """
    points = [x for sublist in points for x in sublist]
    img = Image.new("L", img_dim, 0)
    ImageDraw.Draw(img).polygon(points, outline=1, fill=1)
    img_array = np.asarray(img)
    img_uint8 = np.expand_dims(img_array, axis=2).astype("uint8")
    img_array = np.asfortranarray(img_uint8)
    rs = CocoMask.encode(img_array)
    return rs, img_uint8


def xywh_to_xyxy(xywh):
    """Convert [x1 y1 w h] box format to [x1 y1 x2 y2] format.
    copied from:
    https://github.com/facebookresearch/Detectron/blob/058768239b2d859c7350f633609fddb3a9094a91/detectron/utils/boxes.py#L74
    """
    if isinstance(xywh, (list, tuple)):
        # Single box given as a list of coordinates
        assert len(xywh) == 4
        x1, y1 = xywh[0], xywh[1]
        x2 = x1 + np.maximum(0.0, xywh[2] - 1.0)
        y2 = y1 + np.maximum(0.0, xywh[3] - 1.0)
        return (x1, y1, x2, y2)
    elif isinstance(xywh, np.ndarray):
        # Multiple boxes given as a 2D ndarray
        return np.hstack((xywh[:, 0:2], xywh[:, 0:2] + np.maximum(0, xywh[:, 2:4] - 1)))
    else:
        raise TypeError("Argument xywh must be a list, tuple, or numpy array.")


def extract_product(img, mask, box):
    img = np.asarray(img).copy()
    box = np.int64(box)
    box = xywh_to_xyxy(list(box))
    box = [int(i) for i in box]
    mask = np.tile(mask, 3)  # Hardcoded for three channel images
    np.copyto(img, 0, where=np.invert(mask))
    top_left, bottom_right = box[:2], box[2:]
    extract_img = img[top_left[1] : bottom_right[1], top_left[0] : bottom_right[0]]
    return Image.fromarray(extract_img)


def extract_objects(json_file_loc: str, labels: list, img_root_loc: str, verbose: bool = False):
    js = load_json(json_file_loc)
    img = Image.open(img_root_loc + js["imagePath"])
    img_dim = js["imageWidth"], js["imageHeight"]
    product_masks = []
    try:
        for _, box in enumerate(js["shapes"]):
            box_label = box["label"]

            if box_label not in labels:
                if verbose:
                    print(f"We are ignoring: {box_label} label. It is not present in our labels list")
                continue

            points = box["points"]

            # This is important to remove non-polygons
            if len(points) <= 3:
                if verbose:
                    print(f"Box is not a  polygon points: {points}")
                continue
            rs, mask = encode_polygon(points, img_dim)
            box = CocoMask.toBbox(rs).tolist()
            mask[mask > 1] = 1
            mask = mask == 1
            product_mask = extract_product(img, mask, box[0])
            product_masks.append(product_mask)
        return product_masks
    except:
        print("could not extract {}".format(js["imagePath"]))
        return "hi"


def extract_products_one_label(json_loc: str, labels: str, img_root_loc: str, save_folder: str):
    """
    extract labels from one product
    """
    json_files = glob.glob(json_loc + "/*.json")

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    for i in tqdm(json_files):
        products = extract_objects(i, [labels], img_root_loc)
        loc = i.rsplit("/")[-1].rsplit(".")[0]
        if products!='hi':
            for num, j in enumerate(products):
                save_path = os.path.join(save_folder, loc + "_" + str(num) + ".jpg")
                j.save(save_path)


@click.command()
@click.option("-j", "--json_loc", required=True, help="folder location where json files are stored")
@click.option("-l", "--labels", required=True, help="label name str")
@click.option("-i", "--img_root_loc", required=True, help="folder location of the images")
@click.option("-s", "--save_folder", required=True, help="locations where images have to be stored")
def make_extract_products_one_label(json_loc: str, labels: str, img_root_loc: str, save_folder: str):
    """ extract products from one label
    """
    extract_products_one_label(json_loc, labels, img_root_loc, save_folder)


@click.command()
@click.option("-j", "--json_loc", required=True, help="folder location where json files are stored")
def make_label_counter(json_loc: str):
    labels_counter(json_loc)

