import click
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader

from fractalai.datasets.dataset import get_dataset
from fractalai.engine.utils import get_config


def build_data_loader(config: dict):
    train_dataset, val_dataset = get_dataset(config)
    train_dl = DataLoader(
        train_dataset, batch_size=config["batch_size"], shuffle=True, num_workers=2, drop_last=True
    )  # sk
    val_dl = DataLoader(val_dataset, batch_size=config["batch_size"], shuffle=False, num_workers=2)
    return train_dl, val_dl


@click.command()
@click.option("-c", "--config_path", required=True, help="Path to config file")
def make_data_loader(config_path):
    config = get_config(config_path)
    train_dl, val_dl = build_data_loader(config)
    print("[loading train dl]")
    for i, j in train_dl:
        print(i.shape, j.shape, j.unique(return_counts=True))

    print("[loading val dl]")
    for i, j in val_dl:
        print(i.shape, j.shape)


@click.command()
@click.option("-c", "--config_path", required=True, help="Path to config file")
@click.option("-s", "--save_path", default="class_imbalance.jpg", help="Path to config file")
def class_imbalance_plot(config_path: str, save_path: str):
    config = get_config(config_path)
    dataloader, _ = build_data_loader(config)
    mask_0 = 0.0
    mask_1 = 0.0
    # for num, (img, mask) in tqdm(enumerate(dataloader)):
    for img, mask in dataloader:
        mask_1 += mask.sum().item()
        mask_0 += (mask.nelement() - mask.sum()).item()

    mask_0_percent = (mask_0) / (mask_1 + mask_0)
    mask_1_percent = (mask_1) / (mask_1 + mask_0)
    print(mask_0_percent, mask_1_percent)
    fig = plt.figure(figsize=(12, 6))
    plt.bar(["class_0", "class_1"], [mask_0_percent, mask_1_percent])
    fig.savefig(save_path)


# @click.command()
# @click.option("-c", "--config_path", required=True, help="Path to config file")
# def get_mean_std(config_path: str):
#     config = get_config(config_path)
#     config["post_transform_type"] = False
#     dataloader, _ = build_data_loader(config)
#     mean = 0.0
#     std = 0.0
#     pixel_hist = 0.0
#     for i in tqdm(dataloader):
#         images, labels = i
#         print(images.shape, labels.shape)
#         batch_samples = images.size(0)
#         pixel_hist += images.sum(0)
#         images = images.view(batch_samples, -1, images.size(3)).float()
#         mean += images.mean(1).sum(0)
#         std += images.std(1).sum(0)
#         break
#     print(pixel_hist)

#     mean /= len(dataloader.dataset)
#     std /= len(dataloader.dataset)
#     pixel_hist = pixel_hist.item()
#     pixel_hist /= len(dataloader.dataset)

#     mean /= 255
#     std /= 255

#     print("mean: ", mean)
#     print("std: ", std)

#     fig = plt.figure(figsize=(10, 15))
#     num_channels = mean.item()
#     for ch in range(num_channels):
#         fig.add_subplot(num_channels, 1, ch + 1)
#         plt.hist(pixel_hist[:, :, ch].numpy().ravel())
#         plt.title("Mean pixel values for channel " + str(ch))
#     fig.savefig("hist_mean_channel.png")
