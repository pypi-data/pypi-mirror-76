import inspect

import segmentation_models_pytorch as smp

SEGM = {"unet": smp.Unet, "fpn": smp.FPN}


def build_segm_model(config):
    name = config["decoder_name"]
    if name in SEGM.keys():
        model = SEGM[name]
        keys_required = inspect.getfullargspec(model)
        keys_essentials = keys_required[0][1:]
        fdict = {k: v for k, v in config.items() if k in keys_essentials}
        print(fdict)
    else:
        raise NotImplementedError(f"{name} decoder is not implemented")
    return SEGM[name](**fdict)
