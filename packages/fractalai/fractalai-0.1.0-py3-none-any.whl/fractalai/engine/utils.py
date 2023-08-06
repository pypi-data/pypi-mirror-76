import inspect
import pprint

import click
import yaml
from easydict import EasyDict as edict

from fractalai.classifier.model import ClsModel
from fractalai.segmenter.model import SEGM, build_segm_model


def get_config(conf_file: str):
    """
    parse and load the provided configuration
    :param conf_file: configuration file
    :return: conf => parsed configuration
    """
    with open(conf_file, "r") as file_descriptor:
        data = yaml.load(file_descriptor, Loader=yaml.FullLoader)

    # convert the data into an easyDictionary
    return edict(data)


def get_model(config: dict):
    mtype = config["mtype"]
    if mtype == "classification":
        # model = ClsModel(encoder_name=config.encoder, encoder_weights=config.encoder_pretrained, \
        # classes=config.num_classes, activation=config.activation, *config.decoder)
        model = ClsModel(**config)
    elif mtype == "segmentation":
        model = build_segm_model(config)
    else:
        raise ValueError("type of the model is not defined")
    return model


def get_params_count(config: str, only_trainable=False):
    config_file = get_config(config)
    model = get_model(config_file)
    params_num = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return params_num


@click.command()
@click.option("-c", "--config_path", required=True, help="Path to config file")
def make_model(config_path: str):
    config = get_config(config_path)
    model = get_model(config)
    print(model)


@click.command()
@click.option("-c", "--config_path", required=True, help="Path to config file")
def seg_model_params(config_path: str):
    config = get_config(config_path)
    name = config["decoder_name"]
    if name not in SEGM.keys():
        raise NotImplementedError(f"{name} decoder is not implemented")
    model = SEGM[name]
    keys_required = inspect.getfullargspec(model)
    print("[pprint 3.8 version has sort_dict argument, so defaults and annotations are not exact maps here]")
    pprint.pprint(keys_required.annotations)
    pprint.pprint(keys_required.defaults)
