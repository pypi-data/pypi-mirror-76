import click
import torch
from segmentation_models_pytorch.encoders import get_encoder
from segmentation_models_pytorch.utils.base import Activation

from fractalai.classifier.cls_decoder import get_decoder


class ClsEncoderDecoder(torch.nn.Module):
    def __init__(self, encoder, decoder, activation):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.activation = Activation(activation)

    def forward(self, x):
        """Sequentially pass `x` trough model`s `encoder` and `decoder` (return logits!)
        """
        x = self.encoder(x)
        y = self.decoder(x)
        if isinstance(y, tuple):
            _, out = y
        else:
            out = y
        return out

    def predict(self, x):
        """Inference method. Switch model to `eval` mode, call `.forward(x)`
        and apply activation function (if activation is not `None`) with `torch.no_grad()`

        Args:
            x: 4D torch tensor with shape (batch_size, channels, height, width)

        Return:
            prediction: 4D torch tensor with shape (batch_size, classes, height, width)

        """
        if self.training:
            self.eval()

        with torch.no_grad():
            x = self.forward(x)
            if self.activation:
                x = self.activation(x)

        return x


class ClsModel(ClsEncoderDecoder):
    def __init__(
        self,
        classes: int,
        in_channels: int = 3,
        encoder_depth: int = 5,
        encoder_name: str = "resnet34",
        encoder_pretrained: str = "imagenet",
        activation: str = "sigmoid",
        **kwargs,
    ):

        encoder = get_encoder(encoder_name, in_channels, encoder_depth, weights=encoder_pretrained)
        decoder = get_decoder(classes, encoder, encoder_name=encoder_name, **kwargs["decoder"])
        super().__init__(encoder, decoder, activation)
        self.name = f"u-{encoder_name}"


def build_cls_model(config):
    """
    TODO
    """
    pass


@click.command()
def available_encoders():
    from segmentation_models_pytorch.encoders import encoders

    print(encoders.keys())
